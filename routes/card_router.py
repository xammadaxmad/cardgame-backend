from fastapi import APIRouter, Depends, Request
from controllers import card_controller
from database import connection
from helpers import response_helper
from database import schemas
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/shuffle")
def get_all_cards(db: Session = Depends(connection.connect)):
    return card_controller.get_all_cards(db)
