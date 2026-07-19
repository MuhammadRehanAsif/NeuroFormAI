import gradio as gr
import cv2
import numpy as np
import traceback
from core import ExerciseEngine
from exercises.base_exercise import load_exercise, load_all_exercises
from database.queries import (
    create_workout_session, end_workout_session,
    create_session_detail, update_session_detail,
    log_rep, log_posture_alert,
)


_engine = None


def _get_engine():
    global _engine
    if _engine is None:
        print("[DEBUG] Initializing ExerciseEngine...")
        _engine = ExerciseEngine()
        print("[DEBUG] ExerciseEngine ready.")
    return _engine


def create_exercise_tab(exercise_choices=None):
    """Build the Live Exercise tab with webcam feed and controls."""

    with gr.Tab("Live Exercise") as tab:
        gr.Markdown("## Live Exercise Tracker")

        with gr.Row():
            with gr.Column(scale=1):
                exercise_dropdown = gr.Dropdown(
                    label="Select Exercise",
                    choices=exercise_choices or [],
                    interactive=True,
                )
                side_radio = gr.Radio(
                    choices=["left", "right"],
                    value="left",
                    label="Side",
                )
                input_mode = gr.Radio(
                    choices=["Live Camera", "Upload Video"],
                    value="Live Camera",
                    label="Input Mode",
                )
                mirror_checkbox = gr.Checkbox(
                    label="Mirror Video",
                    value=False,
                    visible=False,
                    info="Enable if uploaded video is NOT a selfie/front-camera recording",
                )
                with gr.Row():
                    start_btn = gr.Button("Start Exercise", variant="primary")
                    stop_btn = gr.Button("Stop Exercise", variant="stop")

                gr.Markdown("### Live Stats")
                rep_count_display = gr.Markdown("**Reps:** 0")
                angle_display = gr.Markdown("**Angle:** — °")
                phase_display = gr.Markdown("**Phase:** —")
                score_display = gr.Markdown("**Avg Form Score:** —")
                timer_display = gr.Markdown("**Time:** 00:00")
                alert_display = gr.Markdown("")

            with gr.Column(scale=2):
                webcam = gr.Image(
                    sources=["webcam"],
                    streaming=True,
                    label="Live Camera",
                    visible=True,
                )
                video_input = gr.Video(
                    sources=["upload"],
                    label="Upload Exercise Video",
                    visible=False,
                )
                output_image = gr.Image(
                    label="Processed Feed",
                    height=480,
                )

        with gr.Row():
            process_video_btn = gr.Button("Process Uploaded Video", visible=False, variant="primary")
            session_summary = gr.Markdown("")

    return {
        "tab": tab,
        "webcam": webcam,
        "video_input": video_input,
        "output_image": output_image,
        "input_mode": input_mode,
        "mirror_checkbox": mirror_checkbox,
        "exercise_dropdown": exercise_dropdown,
        "side_radio": side_radio,
        "start_btn": start_btn,
        "stop_btn": stop_btn,
        "rep_count_display": rep_count_display,
        "angle_display": angle_display,
        "phase_display": phase_display,
        "score_display": score_display,
        "timer_display": timer_display,
        "alert_display": alert_display,
        "session_summary": session_summary,
        "process_video_btn": process_video_btn,
    }


def load_exercise_choices():
    """Load exercise names from database for dropdown."""
    try:
        exercises = load_all_exercises()
        return [e.name for e in exercises]
    except Exception:
        return []


def handle_mode_change(mode):
    """Toggle between camera and video upload."""
    if mode == "Live Camera":
        return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)
    else:
        return gr.update(visible=False), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True)


def handle_start_exercise(exercise_name, side, session_state, exercise_state):
    """Start tracking an exercise."""
    if not session_state or "user_id" not in session_state:
        return "Please login first.", exercise_state

    if not exercise_name:
        return "Please select an exercise.", exercise_state

    try:
        exercise = load_exercise(exercise_name)
        _get_engine().start_exercise(exercise.config, side)

        session_id = create_workout_session(session_state["user_id"])
        detail_id = create_session_detail(session_id, exercise.exercise_id, side)

        exercise_state = {
            "session_id": session_id,
            "detail_id": detail_id,
            "exercise_name": exercise_name,
            "exercise_id": exercise.exercise_id,
            "side": side,
        }

        return f"Started **{exercise_name}** ({side} side). Begin exercising!", exercise_state
    except Exception as e:
        print(f"[DEBUG] Error starting exercise: {e}")
        traceback.print_exc()
        return f"Error: {str(e)}", exercise_state


def handle_stop_exercise(exercise_state, session_state):
    """Stop tracking and save results."""
    if not _get_engine().is_active:
        return "No exercise is currently active.", exercise_state

    summary = _get_engine().stop_exercise()

    if exercise_state and "detail_id" in exercise_state:
        update_session_detail(
            exercise_state["detail_id"],
            summary["reps_completed"],
            summary["form_score"],
            summary["duration_seconds"],
        )
        end_workout_session(
            exercise_state["session_id"],
            summary["reps_completed"],
            summary["form_score"],
        )

    from utils.helpers import format_duration, grade_from_score
    duration_str = format_duration(summary["duration_seconds"])
    grade = grade_from_score(summary["form_score"])

    hold_info = ""
    if summary.get("hold_duration"):
        hold_info = f"\n- **Hold Time:** {summary['hold_duration']:.1f}s"

    summary_text = (
        f"### Session Complete!\n"
        f"- **Exercise:** {exercise_state.get('exercise_name', '—')}\n"
        f"- **Reps:** {summary['reps_completed']}{hold_info}\n"
        f"- **Form Score:** {summary['form_score']}% (Grade: {grade})\n"
        f"- **Duration:** {duration_str}\n"
    )

    exercise_state = {}
    return summary_text, exercise_state


def process_webcam_frame(frame, exercise_state, session_state):
    """Process each webcam frame through the exercise engine."""
    engine = _get_engine()

    empty_stats = ("**Reps:** 0", "**Angle:** — °", "**Phase:** —", "**Avg Form Score:** —", "**Time:** 00:00", "")

    if frame is None:
        return None, *empty_stats

    try:
        if not engine.is_active:
            return frame, *empty_stats

        bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # Flip webcam horizontally so it acts as a mirror (selfie view).
        # This makes MediaPipe's LEFT match the user's visual left on screen.
        bgr_frame = cv2.flip(bgr_frame, 1)
        annotated_frame, stats = engine.process_frame(bgr_frame)
        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)

    except Exception as e:
        print(f"[DEBUG] Error in process_frame: {e}")
        traceback.print_exc()
        return frame, *empty_stats

    _log_to_db(stats, exercise_state)

    return annotated_frame, *_format_stats(stats)


def process_uploaded_video(video_path, mirror, exercise_state, session_state):
    """Process an uploaded video file frame by frame, yielding each processed frame (generator)."""
    engine = _get_engine()
    empty_stats = ("**Reps:** 0", "**Angle:** — °", "**Phase:** —", "**Avg Form Score:** —", "**Time:** 00:00", "")

    print(f"[DEBUG] process_uploaded_video called. video_path={video_path}, mirror={mirror}")
    print(f"[DEBUG] engine.is_active={engine.is_active}, exercise_state={exercise_state}")

    if video_path is None:
        print("[DEBUG] video_path is None")
        yield None, *empty_stats
        return

    if not engine.is_active:
        print("[DEBUG] Engine not active -- did you click 'Start Exercise' first?")
        yield None, "**Click 'Start Exercise' first!**", "**Angle:** — °", "**Phase:** —", "**Avg Form Score:** —", "**Time:** 00:00", "Select an exercise and click Start before processing."
        return

    path_str = str(video_path)
    print(f"[DEBUG] Opening video: {path_str}")

    cap = cv2.VideoCapture(path_str)
    if not cap.isOpened():
        print(f"[DEBUG] Failed to open video file: {path_str}")
        yield None, *empty_stats
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"[DEBUG] Video opened: {total_frames} frames, {fps} fps")

    frame_count = 0
    processed = 0

    while cap.isOpened():
        ret, bgr_frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % 3 != 0:
            continue

        if mirror:
            bgr_frame = cv2.flip(bgr_frame, 1)

        try:
            annotated_frame, stats = engine.process_frame(bgr_frame)
            rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            _log_to_db(stats, exercise_state)
            processed += 1

            yield rgb_frame, *_format_stats(stats)

        except Exception as e:
            print(f"[DEBUG] Video frame {frame_count} error: {e}")
            traceback.print_exc()
            continue

    cap.release()
    print(f"[DEBUG] Video processing done. {processed} frames processed.")


def _log_to_db(stats, exercise_state):
    """Log rep and posture data to database."""
    try:
        if stats.get("rep_completed") and stats.get("rep_data") and exercise_state and "detail_id" in exercise_state:
            rd = stats["rep_data"]
            log_rep(
                exercise_state["detail_id"],
                rd["rep_number"], rd["min_angle"], rd["max_angle"], rd["form_score"],
            )

        if stats.get("posture_alerts") and exercise_state and "detail_id" in exercise_state:
            for alert in stats["posture_alerts"]:
                log_posture_alert(
                    exercise_state["detail_id"],
                    alert["alert_type"], alert["message"], alert["deviation_degrees"],
                )
    except Exception as e:
        print(f"[DEBUG] DB logging error: {e}")


def _format_stats(stats):
    """Format stats dict into display strings."""
    from utils.helpers import format_duration

    rep_text = f"**Reps:** {stats['rep_count']}"
    angle_text = f"**Angle:** {stats['angle']}°"
    phase_text = f"**Phase:** {stats['current_phase']}"
    score_text = f"**Avg Form Score:** {stats['form_score']}%"
    timer_text = f"**Time:** {format_duration(stats['elapsed_seconds'])}"

    if stats.get("hold_duration") is not None:
        rep_text = f"**Hold:** {stats['hold_duration']}s"

    alert_lines = []
    for a in stats.get("posture_alerts", []):
        alert_lines.append(f"Warning: {a['message']} ({a['deviation_degrees']} deg off)")
    alert_text = "\n".join(alert_lines) if alert_lines else "Form looks good!"

    return rep_text, angle_text, phase_text, score_text, timer_text, alert_text
