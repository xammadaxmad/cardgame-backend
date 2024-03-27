from fastapi.responses import JSONResponse
from helpers import misc_helper


def validation_exception(exc):
    misc_helper.print_error(exc)
    try:
        inputs = ""
        message = "Invalid inputs. "
        for error in exc.errors():
            field = error["loc"][1]if error["loc"][1] == None else ""
            if(type(field) == int):
                message = error['ctx']['error']
            else:
                inputs = inputs + field +", "

        inputs = inputs.rstrip(", ")
        message = message+ f"{inputs}"
        jsonContent = {
            "status": "error",
            "message": message
        }
        return JSONResponse(
            status_code=422,
            content=jsonContent,
        )
    except Exception as ex:
        misc_helper.print_error(ex)
        jsonContent = {
            "status": "error",
            "message": "Unprocessable entity"
        }
        return JSONResponse(
            status_code=422,
            content=jsonContent,
        )


def generic_exception(exc):
    print(exc)
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "Something went wrong"},
    )


def http_exception(exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "message": exc.detail},
    )
