import json
import os
from database import models
from sqlalchemy.orm import Session

def upload_cards_to_db(db:Session):
    str_directory = "assets/cards/"
    files = os.listdir(str_directory)
    arr_record = []
    for file in files:
        arrFileInfo = file.split(".")
        str_file_type = arrFileInfo[0][-1]
        str_name = arrFileInfo[0]
        str_image = f'{str_directory}{file}'
        str_type = ""
        if str_file_type == "S":
            str_type = "SPADES"
        elif str_file_type == "D":
            str_type = "DIAMONDS"
        elif str_file_type == "H":
            str_type = "HEARTS"
        elif str_file_type == "C":
            str_type = "CLUBS"

        dict_record = {"name": str_name, "image": str_image, "type": str_type}
        arr_record.append(models.Card(**dict_record))
        db.add_all(arr_record)
        db.commit()