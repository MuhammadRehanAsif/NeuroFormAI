from datetime import datetime


def format_duration(seconds):
    """Format seconds into MM:SS string."""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


def format_datetime(dt):
    """Format a datetime object into a readable string."""
    if isinstance(dt, datetime):
        return dt.strftime("%b %d, %Y  %I:%M %p")
    return str(dt)


def grade_from_score(score):
    """Convert a 0-100 form score to a letter grade."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"
