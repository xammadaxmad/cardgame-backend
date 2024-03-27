from typing import List, Any
from fastapi.responses import JSONResponse


class APIResponse:
    status: str
    message: str
    data: List[Any] = []


def success(message, data=None):
    resp = {
        "status": "success",
        "message": message,
        "data": data if data is not None else [],
    }
    return resp


def error(message="Something went wrong", data=None, status_code=500):
    resp = {
        "status": "error",
        "message": message,
        "data": data if data is not None else [],
    }
    return JSONResponse(resp, status_code=status_code)


def not_found(message="Record not found", data=None, status_code=404):
    resp = {
        "status": "error",
        "message": message,
        "data": data if data is not None else [],
    }
    return JSONResponse(resp, status_code=status_code)


def warning(message, data=None):
    resp = {
        "status": "warning",
        "message": message,
        "data": data if data is not None else [],
    }
    return JSONResponse(resp, status_code=200)
