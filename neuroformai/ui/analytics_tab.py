import gradio as gr
from data_structures import quick_sort, merge_sort
from database.queries import get_leaderboard_data, get_user_exercise_stats, get_user_sessions
from utils.helpers import grade_from_score
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
import numpy as np
from datetime import datetime


def create_analytics_tab():
    """Build the Analytics / Leaderboard tab with charts and custom sorting."""

    with gr.Tab("Analytics") as tab:
        gr.Markdown("## Analytics & Leaderboard")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Leaderboard")
                gr.Markdown("Sorted using custom **Quick Sort** algorithm.")
                leaderboard_sort = gr.Dropdown(
                    label="Sort By",
                    choices=["Total Reps", "Form Score", "Total Sessions"],
                    value="Total Reps",
                )
                leaderboard_btn = gr.Button("Load Leaderboard", variant="primary")
                leaderboard_display = gr.Dataframe(
                    headers=["Rank", "User", "Total Reps", "Avg Form Score", "Sessions"],
                    label="Leaderboard",
                    interactive=False,
                )

            with gr.Column(scale=1):
                gr.Markdown("### Your Stats")
                stats_btn = gr.Button("Load My Stats", variant="primary")
                stats_display = gr.Dataframe(
                    headers=["Exercise", "Total Reps", "Times Done", "Avg Score", "Best Score", "Grade"],
                    label="Per-Exercise Stats",
                    interactive=False,
                )

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Progress Over Time")
                progress_btn = gr.Button("Show Progress Chart")
                progress_chart = gr.Image(label="Reps & Form Score Trend", height=350)

            with gr.Column(scale=1):
                gr.Markdown("### Personal Records")
                records_display = gr.Markdown("Click 'Load My Stats' to see personal records.")

    return {
        "tab": tab,
        "leaderboard_sort": leaderboard_sort,
        "leaderboard_btn": leaderboard_btn,
        "leaderboard_display": leaderboard_display,
        "stats_btn": stats_btn,
        "stats_display": stats_display,
        "progress_btn": progress_btn,
        "progress_chart": progress_chart,
        "records_display": records_display,
    }


def handle_load_leaderboard(sort_by):
    """Load and sort leaderboard using custom quick sort."""
    data = get_leaderboard_data()

    if not data:
        return []

    if sort_by == "Total Reps":
        sorted_data = quick_sort(data, key=lambda x: x.get("total_reps", 0), reverse=True)
    elif sort_by == "Form Score":
        sorted_data = quick_sort(data, key=lambda x: x.get("avg_form_score", 0), reverse=True)
    elif sort_by == "Total Sessions":
        sorted_data = quick_sort(data, key=lambda x: x.get("total_sessions", 0), reverse=True)
    else:
        sorted_data = data

    rows = []
    for i, entry in enumerate(sorted_data):
        rows.append([
            i + 1,
            entry.get("full_name", entry.get("username", "—")),
            entry.get("total_reps", 0),
            f"{entry.get('avg_form_score', 0):.1f}%",
            entry.get("total_sessions", 0),
        ])

    return rows


def handle_load_stats(session_state):
    """Load per-exercise stats for the current user."""
    if not session_state or "user_id" not in session_state:
        return [], "Please login first."

    stats = get_user_exercise_stats(session_state["user_id"])

    if not stats:
        return [], "No workout data yet. Start exercising!"

    sorted_stats = merge_sort(stats, key=lambda x: x.get("total_reps", 0), reverse=True)

    rows = []
    records_lines = ["### Personal Records\n"]

    for entry in sorted_stats:
        grade = grade_from_score(entry.get("avg_form_score", 0))
        rows.append([
            entry.get("exercise_name", "—"),
            entry.get("total_reps", 0),
            entry.get("times_performed", 0),
            f"{entry.get('avg_form_score', 0):.1f}%",
            f"{entry.get('best_form_score', 0):.1f}%",
            grade,
        ])

        records_lines.append(
            f"- **{entry.get('exercise_name', '—')}**: "
            f"{entry.get('total_reps', 0)} total reps, "
            f"best score {entry.get('best_form_score', 0):.1f}%"
        )

    records_text = "\n".join(records_lines)
    return rows, records_text


def handle_progress_chart(session_state):
    """Generate a progress chart showing reps and form score over time."""
    if not session_state or "user_id" not in session_state:
        return None

    sessions = get_user_sessions(session_state["user_id"])

    if not sessions or len(sessions) < 2:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, "Need at least 2 sessions for a chart",
                ha="center", va="center", fontsize=14, color="gray")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        return _fig_to_image(fig)

    sorted_sessions = merge_sort(sessions, key=lambda s: s.get("start_time", datetime.min))

    dates = [s.get("start_time", datetime.min) for s in sorted_sessions]
    reps = [s.get("total_reps", 0) for s in sorted_sessions]
    scores = [s.get("avg_form_score", 0) for s in sorted_sessions]

    fig, ax1 = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor("#1a1a2e")
    ax1.set_facecolor("#1a1a2e")

    color_reps = "#00d4aa"
    color_score = "#ff6b6b"

    ax1.plot(dates, reps, color=color_reps, marker="o", linewidth=2, label="Reps")
    ax1.set_xlabel("Date", color="white")
    ax1.set_ylabel("Total Reps", color=color_reps)
    ax1.tick_params(axis="y", labelcolor=color_reps)
    ax1.tick_params(axis="x", labelcolor="white", rotation=45)

    ax2 = ax1.twinx()
    ax2.plot(dates, scores, color=color_score, marker="s", linewidth=2, linestyle="--", label="Form Score")
    ax2.set_ylabel("Form Score (%)", color=color_score)
    ax2.tick_params(axis="y", labelcolor=color_score)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", facecolor="#2a2a3e", labelcolor="white")

    plt.title("Your Progress Over Time", color="white", fontsize=14)
    plt.tight_layout()

    return _fig_to_image(fig)


def _fig_to_image(fig):
    """Convert matplotlib figure to numpy array for Gradio."""
    fig.canvas.draw()
    buf = fig.canvas.buffer_rgba()
    img = np.asarray(buf)
    plt.close(fig)
    return img
