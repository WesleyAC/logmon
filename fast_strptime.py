from datetime import datetime, timezone, timedelta

def fast_strptime(t):
    """
    This is an alternative to using datetime.strptime for a specific format
    string that is ~2.5x faster.

    The format string that it parses is "%d/%b/%Y:%H:%M:%S %z".
    """
    month_lookup = {
            "Jan": 1,
            "Feb": 2,
            "Mar": 3,
            "Apr": 4,
            "May": 5,
            "Jun": 6,
            "Jul": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec": 12
    }
    day = int(t[:2])
    month = month_lookup[t[3:6]]
    year = int(t[7:11])
    hour = int(t[12:14])
    min = int(t[15:17])
    sec = int(t[18:20])
    tz_dir = -1 if t[21] == "-" else 1
    tz_hour = int(t[22:24]) * tz_dir
    tz_min = int(t[24:26]) * tz_dir
    return datetime(day, month, year, hour, min, sec, 0, timezone(timedelta(hours=tz_hour, minutes=tz_min)))
