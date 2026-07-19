import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gradio as gr
from config import MONGO_URI, MONGO_DB_NAME
from database.seed import initialize_database
from ui.gradio_app import build_app


def main():
    print(f"Connecting to MongoDB: {MONGO_DB_NAME}")
    print("Initializing database...")
    initialize_database()

    print("Building Gradio app...")
    app = build_app()

    print("Launching NeuroFormAI...")
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        theme=gr.themes.Soft(
            primary_hue="teal",
            secondary_hue="blue",
        ),
        css="""
        .gradio-container { max-width: 1200px !important; }
        footer { display: none !important; }
        """,
    )


if __name__ == "__main__":
    main()
