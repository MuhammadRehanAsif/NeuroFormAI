from .connection import get_collection
from .collections import setup_collections

EXERCISES = [
    {
        "name": "Bicep Curl",
        "category": "Arms",
        "difficulty": "Beginner",
        "target_angles": {
            "primary": {"landmarks": ["shoulder", "elbow", "wrist"], "up_threshold": 160, "down_threshold": 40},
        },
        "posture_rules": [
            {"name": "elbow_pinned", "description": "Upper arm should stay vertical",
             "landmarks": ["shoulder", "elbow", "hip"], "min_angle": 160, "max_angle": 200,
             "message": "Keep your elbow pinned to your side"},
        ],
        "side_landmarks": {
            "left": {"shoulder": 11, "elbow": 13, "wrist": 15, "hip": 23},
            "right": {"shoulder": 12, "elbow": 14, "wrist": 16, "hip": 24},
        },
        "phases": ["UP", "DOWN"],
        "rep_sequence": ["UP", "DOWN", "UP"],
    },
    {
        "name": "Squat",
        "category": "Legs",
        "difficulty": "Beginner",
        "target_angles": {
            "primary": {"landmarks": ["hip", "knee", "ankle"], "up_threshold": 160, "down_threshold": 90},
        },
        "posture_rules": [
            {"name": "back_straight", "description": "Back should remain straight",
             "landmarks": ["shoulder", "hip", "knee"], "min_angle": 150, "max_angle": 200,
             "message": "Keep your back straight"},
        ],
        "side_landmarks": {
            "left": {"shoulder": 11, "hip": 23, "knee": 25, "ankle": 27},
            "right": {"shoulder": 12, "hip": 24, "knee": 26, "ankle": 28},
        },
        "phases": ["UP", "DOWN"],
        "rep_sequence": ["UP", "DOWN", "UP"],
    },
    {
        "name": "Push-Up",
        "category": "Full Body",
        "difficulty": "Beginner",
        "target_angles": {
            "primary": {"landmarks": ["shoulder", "elbow", "wrist"], "up_threshold": 160, "down_threshold": 90},
        },
        "posture_rules": [
            {"name": "body_aligned", "description": "Body should be in a straight line",
             "landmarks": ["shoulder", "hip", "ankle"], "min_angle": 160, "max_angle": 200,
             "message": "Keep your body in a straight line, don't sag your hips"},
        ],
        "side_landmarks": {
            "left": {"shoulder": 11, "elbow": 13, "wrist": 15, "hip": 23, "ankle": 27},
            "right": {"shoulder": 12, "elbow": 14, "wrist": 16, "hip": 24, "ankle": 28},
        },
        "phases": ["UP", "DOWN"],
        "rep_sequence": ["UP", "DOWN", "UP"],
    },
    {
        "name": "Shoulder Press",
        "category": "Shoulders",
        "difficulty": "Intermediate",
        "target_angles": {
            "primary": {"landmarks": ["shoulder", "elbow", "wrist"], "up_threshold": 160, "down_threshold": 80},
        },
        "posture_rules": [
            {"name": "no_back_arch", "description": "Avoid excessive back arch",
             "landmarks": ["shoulder", "hip", "knee"], "min_angle": 160, "max_angle": 200,
             "message": "Don't arch your back, keep core tight"},
        ],
        "side_landmarks": {
            "left": {"shoulder": 11, "elbow": 13, "wrist": 15, "hip": 23, "knee": 25},
            "right": {"shoulder": 12, "elbow": 14, "wrist": 16, "hip": 24, "knee": 26},
        },
        "phases": ["DOWN", "UP"],
        "rep_sequence": ["DOWN", "UP", "DOWN"],
    },
    {
        "name": "Lunge",
        "category": "Legs",
        "difficulty": "Intermediate",
        "target_angles": {
            "primary": {"landmarks": ["hip", "knee", "ankle"], "up_threshold": 160, "down_threshold": 85},
        },
        "posture_rules": [
            {"name": "torso_upright", "description": "Torso should remain upright",
             "landmarks": ["shoulder", "hip", "knee"], "min_angle": 150, "max_angle": 200,
             "message": "Keep your torso upright"},
        ],
        "side_landmarks": {
            "left": {"shoulder": 11, "hip": 23, "knee": 25, "ankle": 27},
            "right": {"shoulder": 12, "hip": 24, "knee": 26, "ankle": 28},
        },
        "phases": ["UP", "DOWN"],
        "rep_sequence": ["UP", "DOWN", "UP"],
    },
    {
        "name": "Lateral Raise",
        "category": "Shoulders",
        "difficulty": "Beginner",
        "target_angles": {
            "primary": {"landmarks": ["hip", "shoulder", "elbow"], "up_threshold": 80, "down_threshold": 30},
        },
        "posture_rules": [
            {"name": "arms_straight", "description": "Arms should be nearly straight",
             "landmarks": ["shoulder", "elbow", "wrist"], "min_angle": 150, "max_angle": 200,
             "message": "Keep your arms straight, don't bend elbows"},
        ],
        "side_landmarks": {
            "left": {"shoulder": 11, "elbow": 13, "wrist": 15, "hip": 23},
            "right": {"shoulder": 12, "elbow": 14, "wrist": 16, "hip": 24},
        },
        "phases": ["DOWN", "UP"],
        "rep_sequence": ["DOWN", "UP", "DOWN"],
    },
    {
        "name": "Tricep Extension",
        "category": "Arms",
        "difficulty": "Intermediate",
        "target_angles": {
            "primary": {"landmarks": ["shoulder", "elbow", "wrist"], "up_threshold": 160, "down_threshold": 50},
        },
        "posture_rules": [
            {"name": "upper_arm_vertical", "description": "Upper arm should stay vertical",
             "landmarks": ["hip", "shoulder", "elbow"], "min_angle": 150, "max_angle": 200,
             "message": "Keep your upper arm close to your head"},
        ],
        "side_landmarks": {
            "left": {"shoulder": 11, "elbow": 13, "wrist": 15, "hip": 23},
            "right": {"shoulder": 12, "elbow": 14, "wrist": 16, "hip": 24},
        },
        "phases": ["DOWN", "UP"],
        "rep_sequence": ["DOWN", "UP", "DOWN"],
    },
    {
        "name": "Deadlift",
        "category": "Core",
        "difficulty": "Advanced",
        "target_angles": {
            "primary": {"landmarks": ["shoulder", "hip", "knee"], "up_threshold": 160, "down_threshold": 100},
        },
        "posture_rules": [
            {"name": "back_straight", "description": "Back must remain straight",
             "landmarks": ["shoulder", "hip", "knee"], "min_angle": 150, "max_angle": 200,
             "message": "Keep your back straight, don't round your spine"},
            {"name": "knees_slight_bend", "description": "Maintain slight knee bend",
             "landmarks": ["hip", "knee", "ankle"], "min_angle": 150, "max_angle": 180,
             "message": "Keep a slight bend in your knees"},
        ],
        "side_landmarks": {
            "left": {"shoulder": 11, "hip": 23, "knee": 25, "ankle": 27},
            "right": {"shoulder": 12, "hip": 24, "knee": 26, "ankle": 28},
        },
        "phases": ["UP", "DOWN"],
        "rep_sequence": ["UP", "DOWN", "UP"],
    },
    {
        "name": "Plank",
        "category": "Core",
        "difficulty": "Beginner",
        "target_angles": {
            "primary": {"landmarks": ["shoulder", "hip", "ankle"], "up_threshold": 160, "down_threshold": 160},
        },
        "posture_rules": [
            {"name": "body_aligned", "description": "Body should be in a straight line",
             "landmarks": ["shoulder", "hip", "ankle"], "min_angle": 155, "max_angle": 200,
             "message": "Keep your body straight, don't let hips sag or pike up"},
        ],
        "side_landmarks": {
            "left": {"shoulder": 11, "hip": 23, "ankle": 27},
            "right": {"shoulder": 12, "hip": 24, "ankle": 28},
        },
        "phases": ["HOLD"],
        "rep_sequence": ["HOLD"],
        "is_timed": True,
    },
    {
        "name": "Jumping Jack",
        "category": "Full Body",
        "difficulty": "Beginner",
        "target_angles": {
            "primary": {"landmarks": ["hip", "shoulder", "elbow"], "up_threshold": 150, "down_threshold": 30},
        },
        "posture_rules": [],
        "side_landmarks": {
            "left": {"shoulder": 11, "elbow": 13, "wrist": 15, "hip": 23, "knee": 25, "ankle": 27},
            "right": {"shoulder": 12, "elbow": 14, "wrist": 16, "hip": 24, "knee": 26, "ankle": 28},
        },
        "phases": ["DOWN", "UP"],
        "rep_sequence": ["DOWN", "UP", "DOWN"],
    },
    {
        "name": "High Knees",
        "category": "Full Body",
        "difficulty": "Beginner",
        "target_angles": {
            "primary": {"landmarks": ["shoulder", "hip", "knee"], "up_threshold": 150, "down_threshold": 90},
        },
        "posture_rules": [
            {"name": "torso_upright", "description": "Torso should remain upright",
             "landmarks": ["shoulder", "hip", "knee"], "min_angle": 140, "max_angle": 200,
             "message": "Keep your torso upright, don't lean forward"},
        ],
        "side_landmarks": {
            "left": {"shoulder": 11, "hip": 23, "knee": 25},
            "right": {"shoulder": 12, "hip": 24, "knee": 26},
        },
        "phases": ["DOWN", "UP"],
        "rep_sequence": ["DOWN", "UP", "DOWN"],
    },
    {
        "name": "Leg Raise",
        "category": "Legs",
        "difficulty": "Beginner",
        "target_angles": {
            "primary": {"landmarks": ["shoulder", "hip", "knee"], "up_threshold": 150, "down_threshold": 90},
        },
        "posture_rules": [
            {"name": "standing_leg_straight", "description": "Standing leg should remain straight",
             "landmarks": ["hip", "knee", "ankle"], "min_angle": 160, "max_angle": 200,
             "message": "Keep your standing leg straight"},
        ],
        "side_landmarks": {
            "left": {"shoulder": 11, "hip": 23, "knee": 25, "ankle": 27},
            "right": {"shoulder": 12, "hip": 24, "knee": 26, "ankle": 28},
        },
        "phases": ["DOWN", "UP"],
        "rep_sequence": ["DOWN", "UP", "DOWN"],
    },
    {
        "name": "Front Raise",
        "category": "Shoulders",
        "difficulty": "Beginner",
        "target_angles": {
            "primary": {"landmarks": ["hip", "shoulder", "wrist"], "up_threshold": 80, "down_threshold": 30},
        },
        "posture_rules": [
            {"name": "arms_straight", "description": "Arms should be nearly straight",
             "landmarks": ["shoulder", "elbow", "wrist"], "min_angle": 150, "max_angle": 200,
             "message": "Keep your arms straight"},
        ],
        "side_landmarks": {
            "left": {"shoulder": 11, "elbow": 13, "wrist": 15, "hip": 23},
            "right": {"shoulder": 12, "elbow": 14, "wrist": 16, "hip": 24},
        },
        "phases": ["DOWN", "UP"],
        "rep_sequence": ["DOWN", "UP", "DOWN"],
    },
    {
        "name": "Calf Raise",
        "category": "Legs",
        "difficulty": "Beginner",
        "target_angles": {
            "primary": {"landmarks": ["knee", "ankle", "foot"], "up_threshold": 160, "down_threshold": 140},
        },
        "posture_rules": [
            {"name": "knees_straight", "description": "Knees should remain straight",
             "landmarks": ["hip", "knee", "ankle"], "min_angle": 165, "max_angle": 200,
             "message": "Keep your knees straight"},
        ],
        "side_landmarks": {
            "left": {"hip": 23, "knee": 25, "ankle": 27, "foot": 31},
            "right": {"hip": 24, "knee": 26, "ankle": 28, "foot": 32},
        },
        "phases": ["DOWN", "UP"],
        "rep_sequence": ["DOWN", "UP", "DOWN"],
    },
]


def seed_exercises():
    """Insert all 14 exercise definitions into the database. Skips if already present."""
    exercises_col = get_collection("exercises")

    inserted = 0
    skipped = 0
    for exercise in EXERCISES:
        existing = exercises_col.find_one({"name": exercise["name"]})
        if existing:
            skipped += 1
            continue
        exercises_col.insert_one(exercise)
        inserted += 1

    print(f"Seeded exercises: {inserted} inserted, {skipped} already existed.")


def initialize_database():
    """Full database setup: create collections, indexes, and seed exercises."""
    setup_collections()
    seed_exercises()
    print("Database initialization complete.")
