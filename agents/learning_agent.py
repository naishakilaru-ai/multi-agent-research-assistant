import json
import os

LOG_FILE = "conversation_history.json"


def save_interaction(question, answer, sources):
    """
    Saves each interaction for future learning.
    """

    interaction = {
        "question": question,
        "answer": answer,
        "sources": sources
    }

    if os.path.exists(LOG_FILE):

        with open(LOG_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)

    else:

        history = []

    history.append(interaction)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)