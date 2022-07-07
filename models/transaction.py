from datetime import datetime
from typing import Optional
from models.customer import CreateCustomer, Customer
from models.outlets import Outlet
from pydantic import BaseModel


class TransactionModel(BaseModel):

    amount: float
    date_created: datetime = datetime.now()


class Transaction(TransactionModel):
    id: int
    outlet: Outlet
    reference_number: str
    sender: Customer
    receiver: Customer
    is_done: bool = False


class CreateTransaction(TransactionModel):
    outlet_number: str = ""
    sender: CreateCustomer
    receiver: CreateCustomer
