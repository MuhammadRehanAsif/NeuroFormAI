import gradio as gr

from .login_tab import create_login_tab, handle_login, handle_signup, handle_auto_login
from .exercise_tab import (
    create_exercise_tab, handle_start_exercise, handle_stop_exercise,
    process_webcam_frame, process_uploaded_video, handle_mode_change,
    load_exercise_choices,
)
from .plan_tab import (
    create_plan_tab, handle_add_to_plan, handle_remove_from_plan,
    handle_undo, handle_clear_plan, handle_move_up, handle_move_down,
)
from .history_tab import create_history_tab, handle_load_history, handle_sort, handle_prev, handle_next
from .analytics_tab import (
    create_analytics_tab, handle_load_leaderboard, handle_load_stats, handle_progress_chart,
)


def build_app():
    """Assemble all tabs into the Gradio application."""

    with gr.Blocks(title="NeuroFormAI") as app:

        gr.Markdown("# NeuroFormAI — Your AI Exercise Companion")
        gr.Markdown("Track exercises, monitor your posture, and analyze your progress.")

        session_state = gr.State(value=None)
        exercise_state = gr.State(value={})
        browser_state = gr.BrowserState(
            default_value=None,
            storage_key="neuroformai_auth",
            secret="neuroformai_secret_key_2026",
        )

        exercise_choices = load_exercise_choices()

        login_components = create_login_tab()
        exercise_components = create_exercise_tab(exercise_choices)
        plan_components = create_plan_tab(exercise_choices)
        history_components = create_history_tab()
        analytics_components = create_analytics_tab()

        # ── Login Events ──
        login_components["login_btn"].click(
            fn=handle_login,
            inputs=[
                login_components["login_username"],
                login_components["login_password"],
                session_state,
                browser_state,
            ],
            outputs=[
                login_components["login_msg"],
                login_components["user_status"],
                session_state,
                browser_state,
            ],
        )

        login_components["signup_btn"].click(
            fn=handle_signup,
            inputs=[
                login_components["signup_fullname"],
                login_components["signup_username"],
                login_components["signup_password"],
                session_state,
                browser_state,
            ],
            outputs=[
                login_components["signup_msg"],
                login_components["user_status"],
                session_state,
                browser_state,
            ],
        )

        # Auto-login on page load from saved browser credentials
        app.load(
            fn=handle_auto_login,
            inputs=[browser_state, session_state],
            outputs=[login_components["user_status"], session_state],
        )

        # ── Exercise Events ──

        exercise_components["start_btn"].click(
            fn=handle_start_exercise,
            inputs=[
                exercise_components["exercise_dropdown"],
                exercise_components["side_radio"],
                session_state,
                exercise_state,
            ],
            outputs=[
                exercise_components["session_summary"],
                exercise_state,
            ],
        )

        exercise_components["stop_btn"].click(
            fn=handle_stop_exercise,
            inputs=[exercise_state, session_state],
            outputs=[
                exercise_components["session_summary"],
                exercise_state,
            ],
        )

        exercise_components["input_mode"].change(
            fn=handle_mode_change,
            inputs=[exercise_components["input_mode"]],
            outputs=[
                exercise_components["webcam"],
                exercise_components["video_input"],
                exercise_components["process_video_btn"],
                exercise_components["mirror_checkbox"],
            ],
        )

        exercise_components["webcam"].stream(
            fn=process_webcam_frame,
            inputs=[
                exercise_components["webcam"],
                exercise_state,
                session_state,
            ],
            outputs=[
                exercise_components["output_image"],
                exercise_components["rep_count_display"],
                exercise_components["angle_display"],
                exercise_components["phase_display"],
                exercise_components["score_display"],
                exercise_components["timer_display"],
                exercise_components["alert_display"],
            ],
        )

        exercise_components["process_video_btn"].click(
            fn=process_uploaded_video,
            inputs=[
                exercise_components["video_input"],
                exercise_components["mirror_checkbox"],
                exercise_state,
                session_state,
            ],
            outputs=[
                exercise_components["output_image"],
                exercise_components["rep_count_display"],
                exercise_components["angle_display"],
                exercise_components["phase_display"],
                exercise_components["score_display"],
                exercise_components["timer_display"],
                exercise_components["alert_display"],
            ],
        )

        # ── Plan Events ──

        plan_components["add_btn"].click(
            fn=handle_add_to_plan,
            inputs=[
                plan_components["plan_exercise"],
                plan_components["plan_side"],
                plan_components["plan_sets"],
                plan_components["plan_reps"],
            ],
            outputs=[
                plan_components["plan_display"],
                plan_components["plan_msg"],
                plan_components["plan_summary"],
            ],
        )

        plan_components["remove_btn"].click(
            fn=handle_remove_from_plan,
            inputs=[plan_components["remove_index"]],
            outputs=[
                plan_components["plan_display"],
                plan_components["plan_msg"],
                plan_components["plan_summary"],
            ],
        )

        plan_components["undo_btn"].click(
            fn=handle_undo,
            outputs=[
                plan_components["plan_display"],
                plan_components["plan_msg"],
                plan_components["plan_summary"],
            ],
        )

        plan_components["clear_btn"].click(
            fn=handle_clear_plan,
            outputs=[
                plan_components["plan_display"],
                plan_components["plan_msg"],
                plan_components["plan_summary"],
            ],
        )

        plan_components["move_up_btn"].click(
            fn=handle_move_up,
            inputs=[plan_components["remove_index"]],
            outputs=[
                plan_components["plan_display"],
                plan_components["plan_msg"],
                plan_components["plan_summary"],
            ],
        )

        plan_components["move_down_btn"].click(
            fn=handle_move_down,
            inputs=[plan_components["remove_index"]],
            outputs=[
                plan_components["plan_display"],
                plan_components["plan_msg"],
                plan_components["plan_summary"],
            ],
        )

        # ── History Events ──

        history_components["load_btn"].click(
            fn=handle_load_history,
            inputs=[session_state],
            outputs=[
                history_components["session_display"],
                history_components["session_counter"],
                history_components["details_display"],
            ],
        )

        history_components["sort_btn"].click(
            fn=handle_sort,
            inputs=[history_components["sort_by"], session_state],
            outputs=[
                history_components["session_display"],
                history_components["session_counter"],
                history_components["details_display"],
            ],
        )

        history_components["prev_btn"].click(
            fn=handle_prev,
            outputs=[
                history_components["session_display"],
                history_components["session_counter"],
                history_components["details_display"],
            ],
        )

        history_components["next_btn"].click(
            fn=handle_next,
            outputs=[
                history_components["session_display"],
                history_components["session_counter"],
                history_components["details_display"],
            ],
        )

        # ── Analytics Events ──

        analytics_components["leaderboard_btn"].click(
            fn=handle_load_leaderboard,
            inputs=[analytics_components["leaderboard_sort"]],
            outputs=[analytics_components["leaderboard_display"]],
        )

        analytics_components["stats_btn"].click(
            fn=handle_load_stats,
            inputs=[session_state],
            outputs=[
                analytics_components["stats_display"],
                analytics_components["records_display"],
            ],
        )

        analytics_components["progress_btn"].click(
            fn=handle_progress_chart,
            inputs=[session_state],
            outputs=[analytics_components["progress_chart"]],
        )

    return app
