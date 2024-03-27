from sqlalchemy import (
    DateTime,
    TIMESTAMP,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    Double,
    CHAR,
    Enum,
)
from database import connection
from database.connection import Base
from helpers import datetime_helper

class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    image = Column(String)
    type = Column(String)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    ip_address = Column(String)
    first = Column(Integer,default=0)
    second = Column(Integer,default=0)
    third = Column(Integer,default=0)
    forth = Column(Integer,default=0)


class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True)
    player_1 = Column(Integer, default=0)
    player_2 = Column(Integer, default=0)
    player_3 = Column(Integer, default=0)
    player_4 = Column(Integer, default=0)
    is_started = Column(Integer, default=0)
    is_finished = Column(Integer, default=0)
    room_id = Column(Double,default=0)
    created_at = Column(TIMESTAMP,default=datetime_helper.get_current_datetime())


class RoomCard(Base):
    __tablename__ = "room_cards"
    id = Column(Integer, primary_key=True)
    room_id = Column(Double, default=0)
    card_id = Column(Integer, default=0)
    player_id = Column(Integer, default=0)