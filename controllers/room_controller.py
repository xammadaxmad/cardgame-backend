import time
from sqlalchemy.orm import Session
from database import models, schemas
from helpers import misc_helper, response_helper, data_helper


def get_all_rooms(db: Session):
    data = db.query(models.Room).all()
    arr_return = []
    for dt in data:
        arr_return.append(misc_helper.jsonify_model(dt))
    return response_helper.success("", arr_return)


def get_room_by_id(db: Session, room_id: int):
    data = db.query(models.Room).filter(models.Room.room_id == room_id).first()
    if data is None:
        return response_helper.error("Room not found")
    obj_data = misc_helper.jsonify_model(data)
    obj_data["player_1"] = data_helper.get_user(db, data.player_1)
    obj_data["player_2"] = data_helper.get_user(db, data.player_2)
    obj_data["player_3"] = data_helper.get_user(db, data.player_3)
    obj_data["player_4"] = data_helper.get_user(db, data.player_4)
    return response_helper.success("", obj_data)


def create_room(db: Session, user_id: int):
    try:
        room = models.Room()
        room.player_1 = user_id
        room.room_id = int(time.time() * 1000)
        db.add(room)
        db.commit()
        db.refresh(room)
        return response_helper.success(f"Room#{room.room_id} has been created")
    except Exception as ex:
        misc_helper.print_error(ex)
        return response_helper.error()


def delete_room(db: Session, room_id: int):
    try:
        db.query(models.Room).filter(models.Room.room_id == room_id).delete()
        db.commit()
        return response_helper.success("Room deleted successfully")
    except Exception as ex:
        db.rollback()
        return response_helper.error("Something went wrong")


def join_room(db: Session, room_id: int, user_id: int):
    try:
        print(user_id)
        data = db.query(models.Room).filter(models.Room.room_id == room_id).first()
        if data.player_1 == user_id:
            return response_helper.error("You have already joined", status_code=409)

        if is_room_already_joined(data, user_id):
            return response_helper.error(
                "You have already joined this room", status_code=409
            )

        if data.player_2 < 1:
            data.player_2 = user_id
        elif data.player_3 < 1:
            data.player_3 = user_id
        elif data.player_4 < 1:
            data.player_4 = user_id
        else:
            return response_helper.error(
                f"Room#{room_id} is already full", status_code=409
            )
        db.commit()
        return response_helper.success(f"Room#{room_id} joined successfully")
    except Exception as ex:
        misc_helper.print_error(ex)
        return response_helper.error()


def is_room_already_joined(room: models.Room, user_id: int):
    if room.player_1 == user_id:
        return True
    elif room.player_2 == user_id:
        return True
    elif room.player_3 == user_id:
        return True
    elif room.player_4 == user_id:
        return True
    return False


def start_game(db: Session, room_id: int):
    try:
        data = db.query(models.Room).filter(models.Room.room_id == room_id).first()
        data.is_started = 1
        db.commit()
        data_helper.divide_cards_to_players(db,room_id)
        return response_helper.success("Game has been started")
    except Exception as ex:
        misc_helper.print_error(ex)
        return response_helper.error()


def finish_game(db: Session, room_id: int):
    try:
        data = db.query(models.Room).filter(models.Room.room_id == room_id).first()
        data.is_finished = 1
        db.commit()
        return response_helper.success("Game has been finished")
    except Exception as ex:
        misc_helper.print_error(ex)
        return response_helper.error()


def load_game_data():
    arr_return = {}
    arr_return["player_1"]
    pass
