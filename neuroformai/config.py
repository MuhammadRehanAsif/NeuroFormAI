import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "neuroformai")

MEDIAPIPE_MIN_DETECTION_CONFIDENCE = 0.5
MEDIAPIPE_MIN_TRACKING_CONFIDENCE = 0.5

ANGLE_SMOOTHING_WINDOW = 7

EXERCISE_CATEGORIES = {
    "Arms": ["Bicep Curl", "Tricep Extension"],
    "Shoulders": ["Shoulder Press", "Lateral Raise", "Front Raise"],
    "Legs": ["Squat", "Lunge", "Calf Raise", "Leg Raise"],
    "Full Body": ["Push-Up", "Jumping Jack", "High Knees"],
    "Core": ["Plank", "Deadlift"],
}
