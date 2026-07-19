from data_structures import DynamicArray


class PostureChecker:
    """
    Validates exercise form by checking secondary angles against posture rules.
    Each exercise defines rules like "back should be straight" with angle thresholds.
    Returns active alerts when form deviates from acceptable ranges.
    """

    def __init__(self, posture_rules, side_landmarks):
        self._rules = posture_rules
        self._side_landmarks = side_landmarks
        self._active_alerts = DynamicArray(initial_capacity=8)
        self._alert_cooldowns = {}
        self._cooldown_frames = 30

    def check(self, landmarks, angle_calculator, side):
        """
        Check all posture rules against current landmarks.
        Returns a list of alert dicts for any violations detected.
        """
        self._active_alerts.clear()
        landmark_map = self._side_landmarks.get(side, self._side_landmarks.get("left"))

        for rule in self._rules:
            alert = self._check_rule(rule, landmarks, angle_calculator, landmark_map)
            if alert:
                rule_name = rule["name"]
                if rule_name in self._alert_cooldowns and self._alert_cooldowns[rule_name] > 0:
                    self._alert_cooldowns[rule_name] -= 1
                    continue

                self._active_alerts.append(alert)
                self._alert_cooldowns[rule_name] = self._cooldown_frames

        for name in self._alert_cooldowns:
            if self._alert_cooldowns[name] > 0:
                self._alert_cooldowns[name] -= 1

        return self._active_alerts.to_list()

    def _check_rule(self, rule, landmarks, angle_calculator, landmark_map):
        """Check a single posture rule. Returns alert dict or None."""
        rule_landmarks = rule["landmarks"]

        indices = []
        for lm_name in rule_landmarks:
            if lm_name not in landmark_map:
                return None
            indices.append(landmark_map[lm_name])

        if len(indices) != 3:
            return None

        for idx in indices:
            if idx >= landmarks.size():
                return None

        point_a = landmarks.get(indices[0])
        point_b = landmarks.get(indices[1])
        point_c = landmarks.get(indices[2])

        for pt in [point_a, point_b, point_c]:
            if pt[3] < 0.5:
                return None

        angle = angle_calculator.calculate_angle(point_a, point_b, point_c)

        min_ok = rule.get("min_angle", 0)
        max_ok = rule.get("max_angle", 360)

        if angle < min_ok:
            deviation = min_ok - angle
            return {
                "alert_type": rule["name"],
                "message": rule["message"],
                "deviation_degrees": round(deviation, 1),
                "current_angle": round(angle, 1),
            }
        elif angle > max_ok:
            deviation = angle - max_ok
            return {
                "alert_type": rule["name"],
                "message": rule["message"],
                "deviation_degrees": round(deviation, 1),
                "current_angle": round(angle, 1),
            }

        return None

    def reset(self):
        """Reset alerts and cooldowns for a new exercise."""
        self._active_alerts.clear()
        self._alert_cooldowns.clear()
