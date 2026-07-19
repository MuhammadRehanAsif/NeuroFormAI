import os
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision
from data_structures import DynamicArray
from config import MEDIAPIPE_MIN_DETECTION_CONFIDENCE, MEDIAPIPE_MIN_TRACKING_CONFIDENCE

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models", "pose_landmarker_full.task")

POSE_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 7),
    (0, 4), (4, 5), (5, 6), (6, 8),
    (9, 10),
    (11, 12), (11, 13), (13, 15), (15, 17), (15, 19), (15, 21),
    (12, 14), (14, 16), (16, 18), (16, 20), (16, 22),
    (11, 23), (12, 24), (23, 24),
    (23, 25), (25, 27), (27, 29), (27, 31),
    (24, 26), (26, 28), (28, 30), (28, 32),
]


class PoseDetector:
    """
    Wraps MediaPipe Tasks PoseLandmarker to extract 33 body landmarks from video frames.
    Uses the VIDEO running mode for sequential frame processing.
    Landmarks are stored in a DynamicArray for DSA integration.
    """

    def __init__(self):
        base_options = mp.tasks.BaseOptions(model_asset_path=MODEL_PATH)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            min_pose_detection_confidence=MEDIAPIPE_MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MEDIAPIPE_MIN_TRACKING_CONFIDENCE,
        )
        self._landmarker = vision.PoseLandmarker.create_from_options(options)
        self._landmarks = DynamicArray(initial_capacity=33)
        self._frame_timestamp_ms = 0

    def process_frame(self, frame):
        """
        Process a BGR frame and extract pose landmarks.
        Returns (landmarks_array, raw_result) where landmarks_array is a
        DynamicArray of (x, y, z, visibility) tuples for each of 33 landmarks.
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        self._frame_timestamp_ms += 33  # ~30fps
        result = self._landmarker.detect_for_video(mp_image, self._frame_timestamp_ms)

        self._landmarks.clear()

        if result.pose_landmarks and len(result.pose_landmarks) > 0:
            for lm in result.pose_landmarks[0]:
                self._landmarks.append((
                    lm.x,
                    lm.y,
                    lm.z,
                    lm.visibility if hasattr(lm, 'visibility') and lm.visibility is not None else lm.presence if hasattr(lm, 'presence') and lm.presence is not None else 1.0,
                ))

        return self._landmarks, result

    def get_landmark(self, index):
        """Get a specific landmark by MediaPipe index (0-32)."""
        if index < 0 or index >= self._landmarks.size():
            return None
        return self._landmarks.get(index)

    def draw_landmarks(self, frame, result):
        """Draw pose landmarks and connections on the frame."""
        if not result.pose_landmarks or len(result.pose_landmarks) == 0:
            return frame

        h, w = frame.shape[:2]
        landmarks = result.pose_landmarks[0]

        for connection in POSE_CONNECTIONS:
            start_idx, end_idx = connection
            if start_idx >= len(landmarks) or end_idx >= len(landmarks):
                continue

            start = landmarks[start_idx]
            end = landmarks[end_idx]

            start_pt = (int(start.x * w), int(start.y * h))
            end_pt = (int(end.x * w), int(end.y * h))

            cv2.line(frame, start_pt, end_pt, (0, 220, 0), 2)

        for lm in landmarks:
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)

        return frame

    def close(self):
        self._landmarker.close()
