from sqlalchemy import Column, String
from sqlalchemy.orm import validates
import uuid

from services.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, nullable=False)
    
    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email, "Invalid email format"
        return email
