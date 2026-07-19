from database.queries import get_all_exercises, get_exercise_by_name


class BaseExercise:
    """
    Represents an exercise loaded from the database.
    Provides convenience accessors for the exercise configuration
    needed by ExerciseEngine, RepCounter, and PostureChecker.
    """

    def __init__(self, config):
        self._config = config

    @property
    def name(self):
        return self._config["name"]

    @property
    def category(self):
        return self._config["category"]

    @property
    def difficulty(self):
        return self._config["difficulty"]

    @property
    def exercise_id(self):
        return str(self._config["_id"])

    @property
    def target_angles(self):
        return self._config["target_angles"]

    @property
    def posture_rules(self):
        return self._config.get("posture_rules", [])

    @property
    def side_landmarks(self):
        return self._config.get("side_landmarks", {})

    @property
    def phases(self):
        return self._config.get("phases", ["UP", "DOWN"])

    @property
    def rep_sequence(self):
        return self._config.get("rep_sequence", ["UP", "DOWN", "UP"])

    @property
    def is_timed(self):
        return self._config.get("is_timed", False)

    @property
    def config(self):
        return self._config

    def __repr__(self):
        return f"BaseExercise({self.name})"


def load_exercise(name):
    """Load a single exercise from the database by name."""
    config = get_exercise_by_name(name)
    if config is None:
        raise ValueError(f"Exercise '{name}' not found in database")
    return BaseExercise(config)


def load_all_exercises():
    """Load all exercises from the database."""
    configs = get_all_exercises()
    return [BaseExercise(c) for c in configs]
