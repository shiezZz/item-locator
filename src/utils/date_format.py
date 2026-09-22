from datetime import datetime, timezone, timedelta

PH_TZ = timezone(timedelta(hours=8))

def format_relative_time(timestamp_str: str) -> str:
    if not timestamp_str:
        return "Unknown"

    dt_utc = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)

    dt_ph = dt_utc.astimezone(PH_TZ)
    now_ph = datetime.now(PH_TZ)

    diff = now_ph - dt_ph
    seconds = diff.total_seconds()

    if seconds < 60:
        return "Just now"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 604800:  # 7 days
        days = int(seconds // 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"
    else:
        return dt.strftime("%b %d, %Y")  