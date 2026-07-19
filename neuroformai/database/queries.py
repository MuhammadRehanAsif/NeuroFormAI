from datetime import datetime
from bson import ObjectId
from .connection import get_collection


# ── Users ──

def create_user(username, password_hash, full_name):
    users = get_collection("users")
    doc = {
        "username": username,
        "password_hash": password_hash,
        "full_name": full_name,
        "created_at": datetime.utcnow(),
    }
    result = users.insert_one(doc)
    return str(result.inserted_id)


def get_user_by_username(username):
    users = get_collection("users")
    return users.find_one({"username": username})


def get_user_by_id(user_id):
    users = get_collection("users")
    return users.find_one({"_id": ObjectId(user_id)})


# ── Exercises ──

def get_all_exercises():
    exercises = get_collection("exercises")
    return list(exercises.find())


def get_exercise_by_name(name):
    exercises = get_collection("exercises")
    return exercises.find_one({"name": name})


def get_exercise_by_id(exercise_id):
    exercises = get_collection("exercises")
    return exercises.find_one({"_id": ObjectId(exercise_id)})


# ── Workout Sessions ──

def create_workout_session(user_id):
    sessions = get_collection("workout_sessions")
    doc = {
        "user_id": ObjectId(user_id),
        "start_time": datetime.utcnow(),
        "end_time": None,
        "total_reps": 0,
        "avg_form_score": 0.0,
    }
    result = sessions.insert_one(doc)
    return str(result.inserted_id)


def end_workout_session(session_id, total_reps, avg_form_score):
    sessions = get_collection("workout_sessions")
    sessions.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": {
            "end_time": datetime.utcnow(),
            "total_reps": total_reps,
            "avg_form_score": avg_form_score,
        }},
    )


def get_user_sessions(user_id):
    sessions = get_collection("workout_sessions")
    return list(
        sessions.find({"user_id": ObjectId(user_id)}).sort("start_time", -1)
    )


# ── Session Details ──

def create_session_detail(session_id, exercise_id, side):
    details = get_collection("session_details")
    doc = {
        "session_id": ObjectId(session_id),
        "exercise_id": ObjectId(exercise_id),
        "side": side,
        "reps_completed": 0,
        "form_score": 0.0,
        "duration_seconds": 0,
    }
    result = details.insert_one(doc)
    return str(result.inserted_id)


def update_session_detail(detail_id, reps_completed, form_score, duration_seconds):
    details = get_collection("session_details")
    details.update_one(
        {"_id": ObjectId(detail_id)},
        {"$set": {
            "reps_completed": reps_completed,
            "form_score": form_score,
            "duration_seconds": duration_seconds,
        }},
    )


def get_session_details(session_id):
    details = get_collection("session_details")
    results = list(details.find({"session_id": ObjectId(session_id)}))
    exercises = get_collection("exercises")
    for detail in results:
        exercise = exercises.find_one({"_id": detail["exercise_id"]})
        detail["exercise_name"] = exercise["name"] if exercise else "Unknown"
    return results


# ── Rep Logs ──

def log_rep(detail_id, rep_number, min_angle, max_angle, form_score):
    rep_logs = get_collection("rep_logs")
    doc = {
        "detail_id": ObjectId(detail_id),
        "rep_number": rep_number,
        "min_angle": min_angle,
        "max_angle": max_angle,
        "form_score": form_score,
        "timestamp": datetime.utcnow(),
    }
    rep_logs.insert_one(doc)


def get_rep_logs(detail_id):
    rep_logs = get_collection("rep_logs")
    return list(rep_logs.find({"detail_id": ObjectId(detail_id)}).sort("rep_number", 1))


# ── Posture Alerts ──

def log_posture_alert(detail_id, alert_type, message, deviation_degrees):
    alerts = get_collection("posture_alerts")
    doc = {
        "detail_id": ObjectId(detail_id),
        "alert_type": alert_type,
        "message": message,
        "deviation_degrees": deviation_degrees,
        "timestamp": datetime.utcnow(),
    }
    alerts.insert_one(doc)


def get_posture_alerts(detail_id):
    alerts = get_collection("posture_alerts")
    return list(alerts.find({"detail_id": ObjectId(detail_id)}).sort("timestamp", 1))


# ── Analytics / Leaderboard ──

def get_leaderboard_data():
    """Aggregate total reps and average form score per user."""
    sessions = get_collection("workout_sessions")
    pipeline = [
        {"$group": {
            "_id": "$user_id",
            "total_reps": {"$sum": "$total_reps"},
            "avg_form_score": {"$avg": "$avg_form_score"},
            "total_sessions": {"$sum": 1},
        }},
    ]
    results = list(sessions.aggregate(pipeline))

    users = get_collection("users")
    for entry in results:
        user = users.find_one({"_id": entry["_id"]})
        entry["username"] = user["username"] if user else "Unknown"
        entry["full_name"] = user.get("full_name", "") if user else ""
    return results


def get_user_exercise_stats(user_id):
    """Get per-exercise stats for a user (for progress tracking)."""
    details = get_collection("session_details")
    pipeline = [
        {"$lookup": {
            "from": "workout_sessions",
            "localField": "session_id",
            "foreignField": "_id",
            "as": "session",
        }},
        {"$unwind": "$session"},
        {"$match": {"session.user_id": ObjectId(user_id)}},
        {"$group": {
            "_id": "$exercise_id",
            "total_reps": {"$sum": "$reps_completed"},
            "avg_form_score": {"$avg": "$form_score"},
            "times_performed": {"$sum": 1},
            "best_form_score": {"$max": "$form_score"},
        }},
    ]
    results = list(details.aggregate(pipeline))

    exercises = get_collection("exercises")
    for entry in results:
        exercise = exercises.find_one({"_id": entry["_id"]})
        entry["exercise_name"] = exercise["name"] if exercise else "Unknown"
    return results
