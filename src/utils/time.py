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


def format_datetime_to_string(date_time: datetime) -> str:
    return date_time.strftime('%m/%d/%Y, %H:%M:%S')
