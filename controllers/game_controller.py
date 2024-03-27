from sqlalchemy.orm import Session
from database import models
from helpers import data_helper, response_helper

def get_game_data(db: Session, room_id:int, user_id:int):
    room = db.query(models.Room).filter_by(room_id = room_id).first()
    arr_player_ids = [room.player_1,room.player_2,room.player_3,room.player_4]
    
    for piu in arr_player_ids:
        if user_id == piu:
            arr_player_ids.remove(user_id)
            arr_player_ids.insert(0,user_id)
            break
    
    arr_players = []
    arr_game_data = {}
    
    for pid in arr_player_ids:
        room_cards = data_helper.get_room_cards(db,room_id,pid)
        player = data_helper.get_user(db,pid)
        player_info = {
            "name":player.username,
            "main": True if user_id == pid else False,
            "cards": room_cards,
            "remaining_cards": []
        }
        arr_players.append(player_info)
        
    arr_game_data["room_id"] = room_id
    arr_game_data["players"] = arr_players
        
    
    
    
    return response_helper.success("",arr_game_data)