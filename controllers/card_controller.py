from sqlalchemy.orm import Session
from helpers import response_helper, data_helper
from database import models


def get_all_cards(db: Session):
    data = data_helper.get_shuffled_cards(db)
    return response_helper.success("", data)
