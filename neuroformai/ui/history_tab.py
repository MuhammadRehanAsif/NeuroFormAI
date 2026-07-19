import gradio as gr
from data_structures import DoublyLinkedList, merge_sort
from database.queries import get_user_sessions, get_session_details, get_rep_logs, get_posture_alerts
from utils.helpers import format_datetime, format_duration, grade_from_score


_session_history = DoublyLinkedList()


def create_history_tab():
    """Build the History tab with linked list navigation and custom sorting."""

    with gr.Tab("History") as tab:
        gr.Markdown("## Workout History")
        gr.Markdown(
            "Navigate through your past sessions using a **Doubly Linked List**. "
            "Sort using custom **Merge Sort** algorithm."
        )

        with gr.Row():
            load_btn = gr.Button("Load My History", variant="primary")
            sort_by = gr.Dropdown(
                label="Sort By",
                choices=["Date (Newest)", "Date (Oldest)", "Most Reps", "Best Form Score"],
                value="Date (Newest)",
            )
            sort_btn = gr.Button("Sort")

        with gr.Row():
            prev_btn = gr.Button("← Previous Session")
            session_counter = gr.Markdown("Session 0 of 0")
            next_btn = gr.Button("Next Session →")

        with gr.Row():
            session_display = gr.Markdown("Load your history to see past sessions.")

        with gr.Row():
            details_display = gr.Dataframe(
                headers=["Exercise", "Side", "Reps", "Form Score", "Duration"],
                label="Session Exercises",
                interactive=False,
            )

    return {
        "tab": tab,
        "load_btn": load_btn,
        "sort_by": sort_by,
        "sort_btn": sort_btn,
        "prev_btn": prev_btn,
        "session_counter": session_counter,
        "next_btn": next_btn,
        "session_display": session_display,
        "details_display": details_display,
    }


def handle_load_history(session_state):
    """Load all sessions into the doubly linked list."""
    global _session_history
    _session_history = DoublyLinkedList()

    if not session_state or "user_id" not in session_state:
        return "Please login first.", "Session 0 of 0", []

    sessions = get_user_sessions(session_state["user_id"])

    if not sessions:
        return "No workout sessions found.", "Session 0 of 0", []

    for session in sessions:
        _session_history.append(session)

    _session_history.move_to_head()
    return _render_current_session()


def handle_sort(sort_by, session_state):
    """Sort sessions using custom merge sort and reload the linked list."""
    global _session_history

    if _session_history.is_empty():
        return "No sessions to sort.", "Session 0 of 0", []

    sessions = _session_history.to_list()

    if sort_by == "Date (Newest)":
        sorted_sessions = merge_sort(sessions, key=lambda s: s.get("start_time", 0), reverse=True)
    elif sort_by == "Date (Oldest)":
        sorted_sessions = merge_sort(sessions, key=lambda s: s.get("start_time", 0))
    elif sort_by == "Most Reps":
        sorted_sessions = merge_sort(sessions, key=lambda s: s.get("total_reps", 0), reverse=True)
    elif sort_by == "Best Form Score":
        sorted_sessions = merge_sort(sessions, key=lambda s: s.get("avg_form_score", 0), reverse=True)
    else:
        sorted_sessions = sessions

    _session_history = DoublyLinkedList()
    for s in sorted_sessions:
        _session_history.append(s)
    _session_history.move_to_head()

    return _render_current_session()


def handle_prev():
    """Navigate to previous session in linked list."""
    if _session_history.is_empty():
        return "No sessions loaded.", "Session 0 of 0", []
    _session_history.move_prev()
    return _render_current_session()


def handle_next():
    """Navigate to next session in linked list."""
    if _session_history.is_empty():
        return "No sessions loaded.", "Session 0 of 0", []
    _session_history.move_next()
    return _render_current_session()


def _render_current_session():
    """Render the current session pointed to by the linked list."""
    session = _session_history.current()
    if session is None:
        return "No session to display.", "Session 0 of 0", []

    idx = _session_history.current_index() + 1
    total = _session_history.length()
    counter = f"Session {idx} of {total}"

    start = format_datetime(session.get("start_time", "—"))
    end = format_datetime(session.get("end_time", "—")) if session.get("end_time") else "In progress"
    grade = grade_from_score(session.get("avg_form_score", 0))

    display = (
        f"### Session: {start}\n"
        f"- **End:** {end}\n"
        f"- **Total Reps:** {session.get('total_reps', 0)}\n"
        f"- **Avg Form Score:** {session.get('avg_form_score', 0):.1f}% (Grade: {grade})\n"
    )

    details = get_session_details(str(session["_id"]))
    rows = []
    for d in details:
        rows.append([
            d.get("exercise_name", "—"),
            d.get("side", "—"),
            d.get("reps_completed", 0),
            f"{d.get('form_score', 0):.1f}%",
            format_duration(d.get("duration_seconds", 0)),
        ])

    return display, counter, rows
