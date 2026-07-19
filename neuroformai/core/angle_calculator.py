import math
from data_structures import CircularQueue
from config import ANGLE_SMOOTHING_WINDOW


class AngleCalculator:
    """
    Calculates angles between three body landmarks and maintains
    per-angle CircularQueue smoothing buffers to reduce noise.
    """

    def __init__(self, smoothing_window=None):
        if smoothing_window is None:
            smoothing_window = ANGLE_SMOOTHING_WINDOW
        self._smoothing_window = smoothing_window
        self._smoothing_buffers = {}

    @staticmethod
    def calculate_angle(point_a, point_b, point_c):
        """
        Calculate the angle at point_b formed by points a-b-c.
        Each point is a tuple of (x, y) or (x, y, z, visibility).
        Returns angle in degrees (0-180).
        """
        ax, ay = point_a[0], point_a[1]
        bx, by = point_b[0], point_b[1]
        cx, cy = point_c[0], point_c[1]

        radians = math.atan2(cy - by, cx - bx) - math.atan2(ay - by, ax - bx)
        angle = abs(radians * 180.0 / math.pi)

        if angle > 180.0:
            angle = 360.0 - angle

        return angle

    def get_smoothed_angle(self, angle_name, point_a, point_b, point_c):
        """
        Calculate angle and pass it through a circular queue smoothing buffer.
        Returns the smoothed (averaged) angle value.
        """
        raw_angle = self.calculate_angle(point_a, point_b, point_c)

        if angle_name not in self._smoothing_buffers:
            self._smoothing_buffers[angle_name] = CircularQueue(self._smoothing_window)

        self._smoothing_buffers[angle_name].enqueue(raw_angle)
        return self._smoothing_buffers[angle_name].average()

    def reset_buffer(self, angle_name=None):
        """Reset smoothing buffer(s). If angle_name is None, reset all."""
        if angle_name:
            if angle_name in self._smoothing_buffers:
                self._smoothing_buffers[angle_name].clear()
        else:
            self._smoothing_buffers.clear()

    def get_buffer_values(self, angle_name):
        """Get the current smoothing buffer values for debugging."""
        if angle_name in self._smoothing_buffers:
            return self._smoothing_buffers[angle_name].to_list()
        return []
