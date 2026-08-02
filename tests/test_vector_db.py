from rag.embeddings import get_embedding
from rag.vector_store import add_document, search

# Sample document
text = """
Artificial Intelligence enables machines to perform tasks
that normally require human intelligence.
"""

embedding = get_embedding(text)

# Store it
add_document(
    doc_id="doc1",
    text=text,
    embedding=embedding
)

print("Document stored successfully!")

# Search
query = "What is Artificial Intelligence?"

query_embedding = get_embedding(query)

results = search(query_embedding)

print("\nSearch Results:\n")

print(results["documents"])