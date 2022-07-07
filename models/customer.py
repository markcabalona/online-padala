from typing import Optional
from pydantic import BaseModel


class CustomerModel(BaseModel):
    full_name: Optional[str] = ""
    mobile_number: Optional[str] = ""


class Customer(CustomerModel):
    id: int


class CreateCustomer(CustomerModel):
    pass
