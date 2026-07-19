import gradio as gr
from data_structures import DoublyLinkedList, Stack
from exercises.base_exercise import load_all_exercises


_workout_plan = DoublyLinkedList()
_undo_stack = Stack()


def create_plan_tab(exercise_choices=None):
    """Build the Workout Plan tab using linked list for playlist and stack for undo."""

    with gr.Tab("Workout Plan") as tab:
        gr.Markdown("## Workout Plan Builder")
        gr.Markdown(
            "Build your workout plan by adding exercises. "
            "Exercises are stored in a **Doubly Linked List** and you can undo actions with a **Stack**."
        )

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Add Exercise")
                plan_exercise = gr.Dropdown(label="Exercise", choices=exercise_choices or [], interactive=True)
                plan_side = gr.Radio(choices=["left", "right"], value="left", label="Side")
                plan_sets = gr.Number(label="Target Sets", value=3, precision=0)
                plan_reps = gr.Number(label="Target Reps per Set", value=10, precision=0)

                with gr.Row():
                    add_btn = gr.Button("Add to Plan", variant="primary")
                    undo_btn = gr.Button("Undo", variant="secondary")
                    clear_btn = gr.Button("Clear Plan", variant="stop")

                plan_msg = gr.Markdown("")

            with gr.Column(scale=2):
                gr.Markdown("### Current Plan")
                plan_display = gr.Dataframe(
                    headers=["#", "Exercise", "Side", "Sets", "Reps"],
                    label="Workout Plan",
                    interactive=False,
                )

                with gr.Row():
                    remove_index = gr.Number(label="Remove # (row number)", precision=0, value=1)
                    remove_btn = gr.Button("Remove")
                    move_up_btn = gr.Button("Move Up ↑")
                    move_down_btn = gr.Button("Move Down ↓")

        with gr.Row():
            gr.Markdown("### Plan Summary")
            plan_summary = gr.Markdown("No exercises in plan.")

    return {
        "tab": tab,
        "plan_exercise": plan_exercise,
        "plan_side": plan_side,
        "plan_sets": plan_sets,
        "plan_reps": plan_reps,
        "add_btn": add_btn,
        "undo_btn": undo_btn,
        "clear_btn": clear_btn,
        "plan_msg": plan_msg,
        "plan_display": plan_display,
        "remove_index": remove_index,
        "remove_btn": remove_btn,
        "move_up_btn": move_up_btn,
        "move_down_btn": move_down_btn,
        "plan_summary": plan_summary,
    }


def _plan_to_dataframe():
    """Convert the linked list plan to a list-of-lists for Gradio Dataframe."""
    rows = []
    for i, item in enumerate(_workout_plan.traverse_forward()):
        rows.append([
            i + 1,
            item["exercise"],
            item["side"],
            item["sets"],
            item["reps"],
        ])
    return rows


def _plan_summary_text():
    """Generate a summary of the plan."""
    if _workout_plan.is_empty():
        return "No exercises in plan."
    total_exercises = _workout_plan.length()
    total_sets = sum(item["sets"] for item in _workout_plan.traverse_forward())
    total_reps = sum(item["sets"] * item["reps"] for item in _workout_plan.traverse_forward())
    return (
        f"**Total Exercises:** {total_exercises} | "
        f"**Total Sets:** {total_sets} | "
        f"**Total Target Reps:** {total_reps}"
    )


def handle_add_to_plan(exercise_name, side, sets, reps):
    """Add an exercise to the workout plan (linked list append)."""
    if not exercise_name:
        return _plan_to_dataframe(), "Please select an exercise.", _plan_summary_text()

    item = {
        "exercise": exercise_name,
        "side": side,
        "sets": int(sets),
        "reps": int(reps),
    }
    _workout_plan.append(item)
    _undo_stack.push({"action": "add", "index": _workout_plan.length() - 1, "item": item})

    return _plan_to_dataframe(), f"Added {exercise_name} to plan.", _plan_summary_text()


def handle_remove_from_plan(index):
    """Remove an exercise from the plan by row number."""
    idx = int(index) - 1
    if idx < 0 or idx >= _workout_plan.length():
        return _plan_to_dataframe(), "Invalid row number.", _plan_summary_text()

    removed = _workout_plan.remove_at(idx)
    _undo_stack.push({"action": "remove", "index": idx, "item": removed})

    return _plan_to_dataframe(), f"Removed {removed['exercise']}.", _plan_summary_text()


def handle_undo():
    """Undo the last action using the stack."""
    if _undo_stack.is_empty():
        return _plan_to_dataframe(), "Nothing to undo.", _plan_summary_text()

    action = _undo_stack.pop()

    if action["action"] == "add":
        idx = action["index"]
        if idx < _workout_plan.length():
            _workout_plan.remove_at(idx)
        msg = f"Undid add of {action['item']['exercise']}."
    elif action["action"] == "remove":
        _workout_plan.insert_at(action["index"], action["item"])
        msg = f"Restored {action['item']['exercise']}."
    elif action["action"] == "move":
        item = _workout_plan.remove_at(action["to_index"])
        _workout_plan.insert_at(action["from_index"], item)
        msg = f"Undid move of {action['item']['exercise']}."
    else:
        msg = "Unknown action."

    return _plan_to_dataframe(), msg, _plan_summary_text()


def handle_clear_plan():
    """Clear the entire plan."""
    _workout_plan.clear()
    _undo_stack.clear()
    return _plan_to_dataframe(), "Plan cleared.", _plan_summary_text()


def handle_move_up(index):
    """Move an exercise up in the plan."""
    idx = int(index) - 1
    if idx <= 0 or idx >= _workout_plan.length():
        return _plan_to_dataframe(), "Cannot move up.", _plan_summary_text()

    item = _workout_plan.remove_at(idx)
    _workout_plan.insert_at(idx - 1, item)
    _undo_stack.push({"action": "move", "from_index": idx, "to_index": idx - 1, "item": item})

    return _plan_to_dataframe(), f"Moved {item['exercise']} up.", _plan_summary_text()


def handle_move_down(index):
    """Move an exercise down in the plan."""
    idx = int(index) - 1
    if idx < 0 or idx >= _workout_plan.length() - 1:
        return _plan_to_dataframe(), "Cannot move down.", _plan_summary_text()

    item = _workout_plan.remove_at(idx)
    _workout_plan.insert_at(idx + 1, item)
    _undo_stack.push({"action": "move", "from_index": idx, "to_index": idx + 1, "item": item})

    return _plan_to_dataframe(), f"Moved {item['exercise']} down.", _plan_summary_text()
