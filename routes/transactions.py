from fastapi import APIRouter
from http import HTTPStatus
from typing import List
import crud
from models.transaction import Transaction,CreateTransaction
from database import db

router = APIRouter(
    tags=["transactions"],
    prefix='/transactions'
)


@router.post("/", status_code=HTTPStatus.CREATED, response_model=Transaction)
def create_transaction(input: CreateTransaction):
    result = crud.create_transaction(db=db.connection, transaction=input)
    return result

@router.get('/',status_code =HTTPStatus.OK,response_model = List[Transaction])
def fetch_transactions():
    return crud.fetch_transactions(db=db.connection)

@router.get('/{ref_num}/',status_code =HTTPStatus.OK,response_model = Transaction)
def fetch_single_transactions(ref_num:str):
    return crud.fetch_single_transaction(db=db.connection,ref_num=ref_num)


@router.patch("/{id}/")
def update_transaction(id: int, updated_transaction: CreateTransaction):
    return crud.update_transaction(
        db=db.connection, id=id, updated_transaction=updated_transaction
    )


@router.delete('/{id}/')
def delete_transaction(transaction_id:int):
    return crud.delete_transaction(db=db.connection,transaction_id=transaction_id)