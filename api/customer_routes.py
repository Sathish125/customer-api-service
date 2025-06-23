import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from services.database import get_db
from models.customer import CustomerCreate, CustomerResponse, CustomerUpdate

# Get logger
logger = logging.getLogger("customer-api")
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
    logger.info(f"Attempting to create customer with email: {customer.email}")
    # Check if customer with email already exists
    db_customer = get_customer_by_email(db, email=customer.email)
    if db_customer:
        logger.warning(f"Customer creation failed: Email already exists: {customer.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Customer with this email already exists"
        )
    new_customer = create_customer_service(db=db, customer=customer)
    logger.info(f"Customer created successfully with ID: {new_customer.id}")
    return new_customer

@router.get("/", response_model=List[CustomerResponse])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Fetching customers list with skip={skip}, limit={limit}")
    customers = get_customers(db, skip=skip, limit=limit)
    logger.info(f"Retrieved {len(customers)} customers")
    return customers

@router.get("/{customer_id}", response_model=CustomerResponse)
def read_customer(customer_id: str, db: Session = Depends(get_db)):
    logger.info(f"Fetching customer with ID: {customer_id}")
    db_customer = get_customer_by_id(db, customer_id=customer_id)
    if db_customer is None:
        logger.warning(f"Customer not found with ID: {customer_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Customer not found"
        )
    logger.info(f"Successfully retrieved customer: {customer_id}")
    return db_customer

@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: str, customer: CustomerUpdate, db: Session = Depends(get_db)):
    logger.info(f"Attempting to update customer with ID: {customer_id}")
    db_customer = get_customer_by_id(db, customer_id=customer_id)
    if db_customer is None:
        logger.warning(f"Update failed: Customer not found with ID: {customer_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Customer not found"
        )
    
    # Check if email is being updated and if it's unique
    if customer.email and customer.email != db_customer.email:
        logger.info(f"Email change detected from {db_customer.email} to {customer.email}")
        email_exists = get_customer_by_email(db, email=customer.email)
        if email_exists:
            logger.warning(f"Update failed: Email already exists: {customer.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Customer with this email already exists"
            )
    
    updated_customer = update_customer_service(db=db, customer_id=customer_id, customer=customer)
    logger.info(f"Customer updated successfully: {customer_id}")
    return updated_customer

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: str, db: Session = Depends(get_db)):
    logger.info(f"Attempting to delete customer with ID: {customer_id}")
    db_customer = get_customer_by_id(db, customer_id=customer_id)
    if db_customer is None:
        logger.warning(f"Delete failed: Customer not found with ID: {customer_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Customer not found"
        )
    delete_customer_service(db=db, customer_id=customer_id)
    logger.info(f"Customer deleted successfully: {customer_id}")
    return None
