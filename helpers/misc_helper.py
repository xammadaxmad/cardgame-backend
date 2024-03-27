import datetime
import traceback
from mysqlx import Row
from sqlalchemy.orm import class_mapper
from database import connection, models, dbcontext
from helpers import datetime_helper, misc_helper
from sqlalchemy.orm import Session


def jsonify_model(model_instance):
    """Converts a SQLAlchemy model instance to a dictionary."""
    if model_instance is None:
        return None

    result = {}
    for column in model_instance.__table__.columns:
        column_value = getattr(model_instance, column.name)

        if isinstance(column_value, datetime.datetime):
            column_value = column_value.strftime("%Y-%m-%d %H:%M:%S")

        result[column.name] = column_value

    return result


def print_error(exception: Exception):
    exc_type = type(exception).__name__
    exc_value = str(exception)
    traceback_str = traceback.format_exc()
    print(f"Exception Type: {exc_type}")
    print(f"Exception Value: {exc_value}")
    print(f"Traceback:\n{traceback_str}")


def row_to_dict(row: Row):
    as_dict = row._asdict()
    keys = row._fields
    arr_return = {}
    for key in keys:
        data = as_dict[key]
        if isinstance(data, datetime.datetime):
            data = data.strftime("%Y-%m-%d %H:%M:%S")
            arr_return[key] = data
        else:
            arr_return[key] = data

    return arr_return
