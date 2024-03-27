from datetime import datetime, timedelta


def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")


def get_formatted_date(str_date):
    if str_date:
        formatted_date = datetime.strptime(str_date, "%Y-%m-%d")
        return formatted_date.strftime("%Y-%m-%d")
    else:
        return None


def get_formatted_datetime(str_date):
    if str_date:
        formatted_date = datetime.strptime(str_date, "%Y-%m-%d H:i:s")
        return formatted_date.strftime("%Y-%m-%d H:i:s")
    else:
        return None


def add_days(day_count):
    date = datetime.now() + timedelta(days=day_count)
    return date.strftime("%Y-%m-%d %H:%M:%S")
