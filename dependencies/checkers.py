from datetime import datetime, timedelta, timezone


def check_access(day_access: datetime):
    one_day_ago = datetime.now(timezone.utc) - timedelta(days=1)
    return True if day_access > one_day_ago else False
