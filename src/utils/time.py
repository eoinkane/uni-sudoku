from datetime import datetime, timedelta


def figure_out_time_difference(then: datetime, now: datetime) -> str:
    """helper function to construct a string using the largest time unit

    Args:
        then (datetime): the starting time of the duration
        now (datetime): the closing time of the duration

    Returns:
        str: a string representation of the duration using the largest time unit 
    """ # noqa
    duration = now - then
    if (duration_in_seconds := (duration / timedelta(seconds=1))) < 60:
        return f"{int(duration_in_seconds)} second(s) ago"
    elif (duration_in_minutes := (duration / timedelta(minutes=1))) < 60:
        return f"{int(duration_in_minutes)} minute(s) ago"
    elif (duration_in_hours := (duration / timedelta(hours=1))) < 24:
        return f"{int(duration_in_hours)} hour(s) ago"
    elif (duration_in_days := (duration / timedelta(days=1))) < 7:
        return f"{int(duration_in_days)} day(s) ago"
    elif (duration_in_weeks := (duration / timedelta(weeks=1))) < 4:
        return f"{int(duration_in_weeks)} week(s) ago"
    elif (duration_in_months := (duration / timedelta(months=1))) < 12:
        return f"{int(duration_in_months)} month(s) ago"
    return f"{int(duration / timedelta(years=1))} year(s) ago"


def calculate_time_elapsed(starting_time: datetime) -> timedelta:
    """helper function to calculate the time elapsed since a starting datetime.
    this function returns a timedelta object representation of the duration

    Args:
        starting_time (datetime): the datetime to calculate the elapsed duration from

    Returns:
        timedelta: the elapsed duration
    """ # noqa
    return datetime.now() - starting_time


def calculate_seconds_elapsed(starting_time: datetime) -> int:
    """helper function to calculate the time elapsed since a starting datetime
    this function returns a int representation of the duration, the number of seconds

    Args:
        starting_time (datetime): the datetime to calculate the elapsed duration from

    Returns:
        int: the elasped duration in seconds
    """ # noqa
    return (datetime.now() - starting_time).seconds


def format_time_elapsed_timedelta_to_string(time_elapsed: timedelta) -> str:
    """helper function to format a timedelta object to a string

    Args:
        time_elapsed (timedelta): the time elapsed object to format

    Returns:
        str: _description_
    """

    # calculate the hours, minutes and seconds of the time elapsed
    hours, remainder = divmod(
        time_elapsed.seconds,
        3600
    )
    minutes, seconds = divmod(
        remainder,
        60
    )

    # construct a datetime object with calculated time,
    # and then format it to a string
    return datetime.strptime(
        f"{hours}:{minutes}:{seconds}",
        "%H:%M:%S"
    ).strftime("%H hour(s) %M minute(s) %S second(s)")


def format_datetime_to_string(date_time: datetime) -> str:
    """helper function to format a datetime object to a string

    Args:
        date_time (datetime): the datetime object to format

    Returns:
        str: a string representation of the datetime object
    """
    return date_time.strftime('%m/%d/%Y, %H:%M:%S')
