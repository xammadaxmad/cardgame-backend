from fastapi import APIRouter, Depends, Request
from controllers import room_controller
from database import connection
from helpers import response_helper
from database import schemas
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")
def get_all_rooms(db: Session = Depends(connection.connect)):
    return room_controller.get_all_rooms(db)


@router.get("/join/{room_id}")
def get_room_by_id(
    room_id: int, request: Request, db: Session = Depends(connection.connect)
):
    return room_controller.join_room(db, room_id, request.state.user_id)


@router.get("/start-game/{room_id}")
def get_room_by_id(room_id: int, db: Session = Depends(connection.connect)):
    return room_controller.start_game(db, room_id)


@router.get("/finish-game/{room_id}")
def get_room_by_id(room_id: int, db: Session = Depends(connection.connect)):
    return room_controller.finish_game(db, room_id)


@router.get("/{room_id}")
def get_room_by_id(room_id: int, db: Session = Depends(connection.connect)):
    return room_controller.get_room_by_id(db, room_id)


@router.delete("/{room_id}")
def get_room_by_id(room_id: int, db: Session = Depends(connection.connect)):
    return room_controller.delete_room(db, room_id)


@router.post("/")
def create_room(request: Request, db: Session = Depends(connection.connect)):
    return room_controller.create_room(db, request.state.user_id)
