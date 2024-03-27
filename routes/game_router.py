from fastapi import APIRouter, Depends, Request
from controllers import game_controller
from database import connection
from helpers import response_helper
from database import schemas
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/{room_id}")
def get_all_cards(
    room_id: int, request: Request, db: Session = Depends(connection.connect)
):
    return game_controller.get_game_data(db, room_id, request.state.user_id)
