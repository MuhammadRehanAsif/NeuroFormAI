import time
from .pose_detector import PoseDetector
from .angle_calculator import AngleCalculator
from .rep_counter import RepCounter
from .posture_checker import PostureChecker


class ExerciseEngine:
    """
    Orchestrates the full per-frame pipeline:
    frame -> pose detection -> angle calculation -> rep counting -> posture checking.
    """

    def __init__(self):
        self._pose_detector = PoseDetector()
        self._angle_calculator = AngleCalculator()
        self._rep_counter = None
        self._posture_checker = None
        self._exercise_config = None
        self._side = "left"
        self._is_active = False
        self._start_time = None
        self._form_scores = []

    def start_exercise(self, exercise_config, side="left"):
        """Initialize engine for a specific exercise."""
        self._exercise_config = exercise_config
        self._side = side
        self._rep_counter = RepCounter(exercise_config)
        self._posture_checker = PostureChecker(
            exercise_config.get("posture_rules", []),
            exercise_config.get("side_landmarks", {}),
        )
        self._angle_calculator.reset_buffer()
        self._is_active = True
        self._start_time = time.time()
        self._form_scores = []

    def stop_exercise(self):
        """Stop the current exercise and return summary."""
        self._is_active = False
        duration = int(time.time() - self._start_time) if self._start_time else 0
        avg_score = (
            sum(self._form_scores) / len(self._form_scores)
            if self._form_scores
            else 0.0
        )

        summary = {
            "reps_completed": self._rep_counter.rep_count if self._rep_counter else 0,
            "form_score": round(avg_score, 1),
            "duration_seconds": duration,
            "hold_duration": self._rep_counter.hold_duration if self._rep_counter and self._rep_counter.is_timed else None,
        }
        return summary

    def process_frame(self, frame):
        """
        Process a single video frame through the full pipeline.
        Returns (annotated_frame, stats_dict).
        """
        if not self._is_active or self._exercise_config is None:
            return frame, self._empty_stats()

        landmarks, results = self._pose_detector.process_frame(frame)

        annotated_frame = self._pose_detector.draw_landmarks(frame.copy(), results)

        if landmarks.size() < 33:
            return annotated_frame, self._empty_stats()

        primary = self._exercise_config["target_angles"]["primary"]
        landmark_names = primary["landmarks"]
        side_map = self._exercise_config["side_landmarks"].get(
            self._side, self._exercise_config["side_landmarks"].get("left")
        )

        indices = []
        for name in landmark_names:
            if name in side_map:
                indices.append(side_map[name])
            else:
                return annotated_frame, self._empty_stats()

        if len(indices) != 3:
            return annotated_frame, self._empty_stats()

        point_a = landmarks.get(indices[0])
        point_b = landmarks.get(indices[1])
        point_c = landmarks.get(indices[2])

        for pt in [point_a, point_b, point_c]:
            if pt[3] < 0.5:
                return annotated_frame, self._empty_stats()

        smoothed_angle = self._angle_calculator.get_smoothed_angle(
            "primary", point_a, point_b, point_c
        )

        rep_completed, form_score, rep_data = self._rep_counter.update(smoothed_angle)

        if rep_completed and rep_data:
            self._form_scores.append(form_score)

        posture_alerts = self._posture_checker.check(
            landmarks, self._angle_calculator, self._side
        )

        from utils.visualization import draw_exercise_overlay
        annotated_frame = draw_exercise_overlay(
            annotated_frame, landmarks, indices, smoothed_angle,
            self._rep_counter, posture_alerts, side_map
        )

        elapsed = int(time.time() - self._start_time) if self._start_time else 0
        avg_score = (
            sum(self._form_scores) / len(self._form_scores)
            if self._form_scores
            else 0.0
        )

        stats = {
            "angle": round(smoothed_angle, 1),
            "rep_count": self._rep_counter.rep_count,
            "current_phase": self._rep_counter.current_phase or "—",
            "form_score": round(avg_score, 1),
            "last_rep_score": form_score if rep_completed else None,
            "posture_alerts": posture_alerts,
            "rep_completed": rep_completed,
            "rep_data": rep_data,
            "elapsed_seconds": elapsed,
            "hold_duration": round(self._rep_counter.hold_duration, 1) if self._rep_counter.is_timed else None,
        }
        return annotated_frame, stats

    def _empty_stats(self):
        return {
            "angle": 0.0,
            "rep_count": self._rep_counter.rep_count if self._rep_counter else 0,
            "current_phase": "—",
            "form_score": 0.0,
            "last_rep_score": None,
            "posture_alerts": [],
            "rep_completed": False,
            "rep_data": None,
            "elapsed_seconds": 0,
            "hold_duration": None,
        }

    @property
    def is_active(self):
        return self._is_active

    def close(self):
        self._pose_detector.close()
