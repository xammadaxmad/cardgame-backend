from fastapi import Request
from sqlalchemy.orm import Session
from helpers import response_helper, misc_helper, auth_helper
from database import models,schemas


def get_user_by_id(db: Session, user_id: int):
    data = db.query(models.User).filter(models.User.id == user_id).first()
    return response_helper.success("", misc_helper.jsonify_model(data))


def save(db: Session, request: Request, user: schemas.User):
    try:
        existed_user = db.query(models.User).filter_by(email=user.email).first()
        if existed_user is not None:
            return response_helper.error(
                "This email is already registered", status_code=409
            )
        u = models.User()
        u.username = user.username
        u.password = user.password
        u.email = user.email
        u.ip_address = request.client.host
        db.add(u)
        db.commit()
        return response_helper.success("User has been registered successfully")
    except Exception as ex:
        db.rollback()
        misc_helper.print_error(ex)
        return response_helper.error("Something went wrong")


def login(db: Session, params: schemas.Login):
    data: models.User = (
        db.query(models.User).filter(models.User.email == params.email).first()
    )
    if data is None:
        return response_helper.error(
            "No user found associated with this email", status_code=404
        )
    if data.password == params.password:
        token_data = {"user_id": data.id}
        token = auth_helper.create_access_token(token_data)
        response_data = {
            "username": data.username,
            "email": data.email,
            "token": token,
            "type": "Bearer"
        }
        return response_helper.success("User has been successfully logged in", response_data)
    else:
        return response_helper.error("Wrong password. Try again", status_code=401)
