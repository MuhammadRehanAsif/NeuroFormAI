from .connection import get_database


def setup_collections():
    """Create collections and indexes. Safe to call multiple times."""
    db = get_database()

    existing = db.list_collection_names()

    if "users" not in existing:
        db.create_collection("users")
    db["users"].create_index("username", unique=True)

    if "exercises" not in existing:
        db.create_collection("exercises")
    db["exercises"].create_index("name", unique=True)

    if "workout_sessions" not in existing:
        db.create_collection("workout_sessions")
    db["workout_sessions"].create_index([("user_id", 1), ("start_time", -1)])

    if "session_details" not in existing:
        db.create_collection("session_details")
    db["session_details"].create_index("session_id")

    if "rep_logs" not in existing:
        db.create_collection("rep_logs")
    db["rep_logs"].create_index("detail_id")

    if "posture_alerts" not in existing:
        db.create_collection("posture_alerts")
    db["posture_alerts"].create_index("detail_id")

    print("Database collections and indexes ready.")
