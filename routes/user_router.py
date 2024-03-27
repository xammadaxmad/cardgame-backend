from fastapi import APIRouter, Depends, Request
from controllers import user_controller
from database import connection
from helpers import response_helper
from database import schemas
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(connection.connect)):
    return user_controller.get_user_by_id(db, user_id)


@router.post("/login")
def get_user_by_id(params: schemas.Login, db: Session = Depends(connection.connect)):
    return user_controller.login(db, params)


@router.post("/register")
def get_user_by_id(
    params: schemas.User, request: Request, db: Session = Depends(connection.connect)
):
    return user_controller.save(db, request, params)
