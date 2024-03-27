import json
from typing import List
from sqlalchemy.orm import Session
from database import models
from helpers import response_helper, data_helper,misc_helper
import random


def get_shuffled_cards(db: Session):
    data = db.query(models.Card).all()
    random.shuffle(data)
    print(data)
    return data


def get_user(db: Session, user_id: int):
    data = db.query(models.User).filter(models.User.id == user_id).first()
    if data is not None:
        del data.password
        del data.ip_address
        return data
    else:
        return None


def divide_cards_to_players(db: Session, room_id: int):

    room = db.query(models.Room).filter(models.Room.room_id == room_id).first()
    arr_player_ids = []
    arr_player_ids.append(room.player_1)
    arr_player_ids.append(room.player_2)
    arr_player_ids.append(room.player_3)
    arr_player_ids.append(room.player_4)

    cards = get_shuffled_cards(db)
    number_of_cards_per_player = len(cards) / 4
    for i in range(4):
        start_index = int(number_of_cards_per_player * i)
        end_index = int(number_of_cards_per_player * (i + 1))
        cards_in_hand = cards[start_index:end_index]
        save_cards_to_room(db, room_id, arr_player_ids[i], cards_in_hand)
    return True


def save_cards_to_room(
    db: Session, room_id: int, player_id: int, cards: List[models.Card]
):
    arr_rc = []
    for card in cards:
        rc = models.RoomCard()
        rc.player_id = player_id
        rc.card_id = card.id
        rc.room_id = room_id
        arr_rc.append(rc)
    db.add_all(arr_rc)
    db.commit()


def get_room_cards(db:Session, room_id:int,player_id:int):
    room_cards = db.query(models.RoomCard).filter_by(room_id = room_id).filter_by(player_id = player_id).all()
    arr_cards = []
    for rc in room_cards:
        arr_card = db.query(models.Card).filter_by(id = rc.card_id).first()
        arr_cards.append(misc_helper.jsonify_model(arr_card))
    return arr_cards


