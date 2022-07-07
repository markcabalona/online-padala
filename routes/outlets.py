from fastapi import APIRouter
from http import HTTPStatus
from typing import List
import crud
from models.outlets import CreateOutlet, Outlet
from database import db

router = APIRouter(tags=["outlets"], prefix="/outlets")


@router.get("/", status_code=HTTPStatus.OK, response_model=List[Outlet])
def fetch_all_outlets():
    return crud.fetch_outlets(db.connection)


@router.post("/", status_code=HTTPStatus.CREATED, response_model=Outlet)
def create_outlet(outlet:CreateOutlet):
    return crud.create_outlet(
        db=db.connection,
        outlet=outlet,
    )
