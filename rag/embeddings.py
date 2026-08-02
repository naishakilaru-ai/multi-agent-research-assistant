import ollama


def get_embedding(text: str) -> list:
    """
    Generate an embedding using Ollama.
    """

    response = ollama.embed(
        model="nomic-embed-text",
        input=text
    )

    return response["embeddings"][0]