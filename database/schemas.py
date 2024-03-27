from pydantic import BaseModel
from typing import Optional
from datetime import date
from helpers import datetime_helper


class User(BaseModel):
    username: str
    email: str
    password: str


class Login(BaseModel):
    email: str
    password: str
