from sqlalchemy.orm import Session
import uuid

from models.db_models import Customer
from models.customer import CustomerCreate, CustomerUpdate


def get_customer_by_id(db: Session, customer_id: str):
    return db.query(Customer).filter(Customer.id == customer_id).first()


def get_customer_by_email(db: Session, email: str):
    return db.query(Customer).filter(Customer.email == email).first()


def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer).offset(skip).limit(limit).all()


def create_customer(db: Session, customer: CustomerCreate):
    db_customer = Customer(
        id=str(uuid.uuid4()),
        first_name=customer.first_name,
        middle_name=customer.middle_name,
        last_name=customer.last_name,
        email=customer.email,
        phone_number=customer.phone_number
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def update_customer(db: Session, customer_id: str, customer: CustomerUpdate):
    db_customer = get_customer_by_id(db, customer_id=customer_id)
    
    update_data = customer.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_customer, key, value)
    
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def delete_customer(db: Session, customer_id: str):
    db_customer = get_customer_by_id(db, customer_id=customer_id)
    db.delete(db_customer)
    db.commit()
    return db_customer
