from data_structures import Stack, DynamicArray


class RepCounter:
    """
    Stack-based state machine for counting exercise repetitions.

    Each exercise has a defined phase sequence (e.g., UP -> DOWN -> UP = 1 rep).
    The stack tracks phase transitions. A rep is counted when the correct
    sequence completes.
    """

    def __init__(self, exercise_config):
        self._phase_stack = Stack()
        self._rep_count = 0
        self._current_phase = None

        self._up_threshold = exercise_config["target_angles"]["primary"]["up_threshold"]
        self._down_threshold = exercise_config["target_angles"]["primary"]["down_threshold"]
        self._rep_sequence = exercise_config.get("rep_sequence", ["UP", "DOWN", "UP"])
        self._is_timed = exercise_config.get("is_timed", False)

        self._min_angle_in_rep = float("inf")
        self._max_angle_in_rep = float("-inf")

        self._rep_angles = DynamicArray(initial_capacity=32)

        self._hold_start_time = None
        self._hold_duration = 0

    def update(self, angle):
        """
        Process a new angle reading and determine phase transitions.
        Returns (rep_completed: bool, form_score: float, rep_data: dict or None).
        """
        if self._is_timed:
            return self._update_timed(angle)

        self._min_angle_in_rep = min(self._min_angle_in_rep, angle)
        self._max_angle_in_rep = max(self._max_angle_in_rep, angle)
        self._rep_angles.append(angle)

        new_phase = self._detect_phase(angle)

        if new_phase is None or new_phase == self._current_phase:
            return False, 0.0, None

        self._current_phase = new_phase
        self._phase_stack.push(new_phase)

        if self._check_rep_complete():
            self._rep_count += 1
            form_score = self._calculate_form_score()
            rep_data = {
                "rep_number": self._rep_count,
                "min_angle": self._min_angle_in_rep,
                "max_angle": self._max_angle_in_rep,
                "form_score": form_score,
            }

            self._reset_rep_tracking()
            return True, form_score, rep_data

        return False, 0.0, None

    def _update_timed(self, angle):
        """For timed exercises like plank, track hold duration."""
        import time

        in_position = angle >= self._up_threshold - 10

        if in_position:
            if self._hold_start_time is None:
                self._hold_start_time = time.time()
            self._hold_duration = time.time() - self._hold_start_time
        else:
            self._hold_start_time = None

        return False, 0.0, None

    def _detect_phase(self, angle):
        """Determine the current movement phase based on angle."""
        if angle >= self._up_threshold:
            return "UP"
        elif angle <= self._down_threshold:
            return "DOWN"
        return None

    def _check_rep_complete(self):
        """Check if the phase stack matches the expected rep sequence."""
        stack_list = self._phase_stack.to_list()
        seq_len = len(self._rep_sequence)

        if len(stack_list) < seq_len:
            return False

        recent = stack_list[-seq_len:]
        return recent == self._rep_sequence

    def _calculate_form_score(self):
        """
        Score the rep quality (0-100) based on how close the angles
        were to the ideal thresholds.
        """
        angle_range = self._max_angle_in_rep - self._min_angle_in_rep
        ideal_range = self._up_threshold - self._down_threshold

        if ideal_range == 0:
            return 100.0

        range_score = min(angle_range / ideal_range, 1.0) * 100

        depth_score = 100.0
        if self._min_angle_in_rep > self._down_threshold + 15:
            depth_score -= (self._min_angle_in_rep - self._down_threshold - 15) * 2
        if self._max_angle_in_rep < self._up_threshold - 15:
            depth_score -= (self._up_threshold - 15 - self._max_angle_in_rep) * 2
        depth_score = max(depth_score, 0.0)

        return round((range_score * 0.5 + depth_score * 0.5), 1)

    def _reset_rep_tracking(self):
        """Reset tracking for the next rep."""
        self._phase_stack.clear()
        if self._current_phase:
            self._phase_stack.push(self._current_phase)
        self._min_angle_in_rep = float("inf")
        self._max_angle_in_rep = float("-inf")
        self._rep_angles.clear()

    @property
    def rep_count(self):
        return self._rep_count

    @property
    def current_phase(self):
        return self._current_phase

    @property
    def hold_duration(self):
        return self._hold_duration

    @property
    def is_timed(self):
        return self._is_timed

    def reset(self):
        """Full reset for starting a new exercise."""
        self._phase_stack.clear()
        self._rep_count = 0
        self._current_phase = None
        self._min_angle_in_rep = float("inf")
        self._max_angle_in_rep = float("-inf")
        self._rep_angles.clear()
        self._hold_start_time = None
        self._hold_duration = 0
