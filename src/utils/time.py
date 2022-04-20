from datetime import datetime, timedelta


def figure_out_time_difference(then: datetime, now: datetime):
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


def update_time_elapsed_time_delta(
    starting_date_time: datetime,
    time_elapsed_time_delta: timedelta
):
    using = time_elapsed_time_delta + (datetime.now() - starting_date_time)
    new = datetime.now()
    print(
        f"\nstart datetime {starting_date_time}"
        f"\n new datetime {new}"
        f"\n diff {new - starting_date_time}"
        f"\n should be {starting_date_time + (new - starting_date_time)}"
        f"\n propsoed {using}"
    )
    return using


def calculate_time_elapsed(starting_time: datetime) -> timedelta:
    return datetime.now() - starting_time


def calculate_seconds_elapsed(starting_time: datetime) -> int:
    return (datetime.now() - starting_time).seconds


# dont use/ maybe do
def format_time_elapsed_timedelta_to_string(time_elapsed):
    hours, remainder = divmod(
        time_elapsed.seconds,
        3600
    )
    minutes, seconds = divmod(
        remainder,
        60
    )
    return datetime.strptime(
        f"{hours}:{minutes}:{seconds}",
        "%H:%M:%S"
    ).strftime("%H hour(s) %M minute(s) %S second(s)")


def format_datetime_to_string(date_time: datetime) -> str:
    return date_time.strftime('%m/%d/%Y, %H:%M:%S')
