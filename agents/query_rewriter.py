import ollama
from config import OLLAMA_MODEL


def rewrite_query(question: str, history: str):

    prompt = f"""
You are a query rewriting assistant.

Your task is to rewrite follow-up questions so they become complete,
standalone questions suitable for semantic search.

If the question is already complete,
return it unchanged.

Conversation History:

{history}

Current Question:

{question}

Standalone Search Query:
"""

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()