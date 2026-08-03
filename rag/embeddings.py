from sentence_transformers import SentenceTransformer

# Load the model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text: str) -> list:
    """
    Generate an embedding for the given text.
    """
    return model.encode(text).tolist()