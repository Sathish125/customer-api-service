from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from services.database import get_db
from models.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from services.customer_service import (
    create_customer as create_customer_service,
    get_customer_by_id,
    get_customers,
    update_customer as update_customer_service,
    delete_customer as delete_customer_service,
    get_customer_by_email
)

router = APIRouter()

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    # Check if customer with email already exists
    db_customer = get_customer_by_email(db, email=customer.email)
    if db_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Customer with this email already exists"
        )
    return create_customer_service(db=db, customer=customer)

@router.get("/", response_model=List[CustomerResponse])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = get_customers(db, skip=skip, limit=limit)
    return customers

@router.get("/{customer_id}", response_model=CustomerResponse)
def read_customer(customer_id: str, db: Session = Depends(get_db)):
    db_customer = get_customer_by_id(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Customer not found"
        )
    return db_customer

@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: str, customer: CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = get_customer_by_id(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Customer not found"
        )
    
    # Check if email is being updated and if it's unique
    if customer.email and customer.email != db_customer.email:
        email_exists = get_customer_by_email(db, email=customer.email)
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Customer with this email already exists"
            )
    
    return update_customer_service(db=db, customer_id=customer_id, customer=customer)

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: str, db: Session = Depends(get_db)):
    db_customer = get_customer_by_id(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Customer not found"
        )
    delete_customer_service(db=db, customer_id=customer_id)
    return None
