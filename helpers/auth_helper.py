from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from controllers import user_controller
from dotenv import load_dotenv
from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt
from database import models, dbcontext, connection
import os
from sqlalchemy.orm import Session

from helpers import misc_helper
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

is_loggedin = OAuth2PasswordBearer(tokenUrl="/api/login")

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
ALGORITHM = os.getenv("ALGORITHM")

OPEN_ROUTES = [
    "/api/user/login",
    "/api/user/register",
    "/api/docs",
    "/docs/openapi.json",
    "/openapi.json",
    "/api/generate-password",
    "/api/docs/openapi.json"
]


def verify_auth_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "status": "success",
            "message": "Authorization successful",
            "data": payload,
        }
    except JWTError as err:
        message = ""
        if "expired" in str(err):
            message = "Authorization Token is expired"
        else:
            message = "Authorization Token is invalid"

        return {"status": "unauthorized", "message": message}


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def is_logged_in_middleware(request: Request, call_next):
    if request.method == "OPTIONS" or request.url.path.startswith("/assets"):
         response = await call_next(request)
         return response
    if request.url.path not in OPEN_ROUTES:
        auth_token = request.headers.get("Authorization")
        if not auth_token:
            return JSONResponse(
                content={
                    "status": "unauthorized",
                    "message": "Authorization Token is missing",
                },
                status_code=401,
            )

        if not auth_token.startswith("Bearer"):
            return JSONResponse(
                content={
                    "status": "unauthorized",
                    "message": "Authorization Token is invalid",
                },
                status_code=401,
            )

        payload = verify_auth_token(auth_token.replace("Bearer ", ""))
        if payload["status"] == "success":
            user_id = payload["data"]["user_id"]
            request.state.user_id = user_id
        else:
            return JSONResponse(content=payload, status_code=401)
    response = await call_next(request)
    return response


def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_pwd


def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
