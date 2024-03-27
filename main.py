from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from database import connection
from helpers import response_helper, env_helper, auth_helper
import pymysql
from exceptions import custom_exceptions
from scripts import upload_cards
from sqlalchemy.orm import Session
from routes import card_router, user_router, room_router, game_router

pymysql.install_as_MySQLdb()
open_api_url = env_helper.get_env("OPEN_API_URL")
app = FastAPI(openapi_url=open_api_url, docs_url="/api/docs")

origins = ["*"]
app.mount("/assets/", StaticFiles(directory="assets/"), name="assets")



# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     return custom_exceptions.validation_exception(exc)


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return custom_exceptions.generic_exception(exc)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return custom_exceptions.http_exception(exc)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(auth_helper.is_logged_in_middleware)

app.include_router(user_router.router, prefix="/api/user",tags=["User"])
app.include_router(room_router.router, prefix="/api/room",tags=["Room"])
app.include_router(card_router.router, prefix="/api/card",tags=["Card"])
app.include_router(game_router.router, prefix="/api/game",tags=["Game"])


@app.get("/api/")
async def test(db: Session = Depends(connection.connect)):
    # files = upload_cards.upload_cards_to_db(db)
    return response_helper.success("Backend server is running...")
