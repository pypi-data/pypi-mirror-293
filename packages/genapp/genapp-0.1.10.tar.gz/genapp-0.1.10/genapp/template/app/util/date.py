from datetime import datetime, timedelta


def str_to_datetime(date_str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")


def date_to_str(date_time) -> str:
    if isinstance(date_time, datetime):
        return date_time.strftime("%Y-%m-%d")
    else:
        raise ValueError("Input must be a datetime object")


def timestamp_to_str(date_time) -> str:
    if isinstance(date_time, datetime):
        return date_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    else:
        raise ValueError("Input must be a datetime object")


def str_to_date(str_date) -> datetime:
    try:
        return datetime.strptime(str_date, "%Y-%m-%d")

    except Exception as e:
        print("ERROR: date -> str_to_date: " + str(e))


def str_to_day_init_datetime(str_date) -> datetime:
    try:
        date = datetime.strptime(str_date, "%Y-%m-%d")
        init_of_day = date.replace(hour=00, minute=00, second=00)
        return init_of_day

    except Exception as e:
        print("ERROR: date -> str_to_day_init_datetime: " + str(e))


def str_to_day_end_datetime(str_date) -> datetime:
    try:
        date = datetime.strptime(str_date, "%Y-%m-%d")
        end_of_day = date.replace(hour=23, minute=59, second=59)
        return end_of_day
    except Exception as e:
        print("ERROR: date -> str_to_day_end_datetime: " + str(e))


def get_str_timestamp() -> datetime:
    try:
        # Obtiene la fecha y hora actual en UTC
        return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
    except Exception as e:
        print("ERROR: date -> get_timestamp: " + str(e))


def get_timestamp() -> datetime:
    try:
        # Obtiene la fecha y hora actual en UTC
        current_time = datetime.utcnow()
        # Elimina los microsegundos
        current_time = current_time.replace(microsecond=0)
        return current_time
    except Exception as e:
        print("ERROR: date -> get_timestamp: " + str(e))
        return None


def get_timestamps_now_delta(delta) -> datetime:
    """
        Devuelve el timestamp en UTC actual

        * si el delta esta (-) now - delta
        * si el delta esta (+) now + delta

    Args:
        delta (int): Delta en segundos

    Returns:
        now, timestamp_delta: _description_
    """
    try:
        now = datetime.utcnow()
        timestamp_delta = now + timedelta(seconds=delta)

        return now, timestamp_delta

    except Exception as e:
        print("ERROR: date -> get_timestamps_now_delta: " + str(e))
