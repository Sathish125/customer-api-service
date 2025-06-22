from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class CustomerBase(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email: EmailStr
    phone_number: str


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None


class CustomerResponse(CustomerBase):
    id: str

    class Config:
        orm_mode = True  # This is the correct setting for Pydantic v1.x
