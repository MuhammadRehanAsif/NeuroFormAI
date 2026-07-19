import cv2
import numpy as np


def draw_exercise_overlay(frame, landmarks, primary_indices, angle, rep_counter, posture_alerts, side_map):
    """
    Draw angle arc, rep count, phase, and posture alerts on the frame.
    """
    h, w = frame.shape[:2]

    if len(primary_indices) == 3 and landmarks.size() >= 33:
        pts = []
        for idx in primary_indices:
            lm = landmarks.get(idx)
            pts.append((int(lm[0] * w), int(lm[1] * h)))

        for pt in pts:
            cv2.circle(frame, pt, 8, (0, 255, 255), -1)
        cv2.line(frame, pts[0], pts[1], (255, 255, 0), 2)
        cv2.line(frame, pts[1], pts[2], (255, 255, 0), 2)

        cv2.putText(
            frame, f"{int(angle)} deg",
            (pts[1][0] + 15, pts[1][1] - 15),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2,
        )

    _draw_stats_panel(frame, rep_counter, angle, posture_alerts)

    return frame


def _draw_stats_panel(frame, rep_counter, angle, posture_alerts):
    """Draw a semi-transparent stats panel in the top-left corner."""
    h, w = frame.shape[:2]
    panel_w, panel_h = 280, 160
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (10 + panel_w, 10 + panel_h), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    y = 40
    if rep_counter.is_timed:
        cv2.putText(frame, f"Hold: {rep_counter.hold_duration:.1f}s",
                    (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    else:
        cv2.putText(frame, f"Reps: {rep_counter.rep_count}",
                    (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    y += 35
    cv2.putText(frame, f"Angle: {int(angle)} deg",
                (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    y += 30
    phase = rep_counter.current_phase or "—"
    cv2.putText(frame, f"Phase: {phase}",
                (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    y += 30
    status_color = (0, 255, 0) if not posture_alerts else (0, 0, 255)
    status_text = "Form: GOOD" if not posture_alerts else "Form: FIX"
    cv2.putText(frame, status_text,
                (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)

    if posture_alerts:
        alert_y = 10 + 160 + 30
        for alert in posture_alerts[:3]:
            overlay2 = frame.copy()
            cv2.rectangle(overlay2, (10, alert_y - 22), (10 + panel_w + 80, alert_y + 8), (0, 0, 150), -1)
            cv2.addWeighted(overlay2, 0.6, frame, 0.4, 0, frame)
            msg = alert["message"]
            if len(msg) > 40:
                msg = msg[:37] + "..."
            cv2.putText(frame, f"! {msg}",
                        (15, alert_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 255), 2)
            alert_y += 35


def draw_progress_bar(frame, x, y, width, height, progress, color=(0, 255, 0)):
    """Draw a progress bar on the frame."""
    progress = max(0.0, min(1.0, progress))
    cv2.rectangle(frame, (x, y), (x + width, y + height), (100, 100, 100), 2)
    fill_w = int(width * progress)
    cv2.rectangle(frame, (x, y), (x + fill_w, y + height), color, -1)
