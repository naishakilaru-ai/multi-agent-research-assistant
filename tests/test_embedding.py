from rag.embeddings import get_embedding

try:
    text = "Artificial Intelligence is transforming education."

    embedding = get_embedding(text)

    print("✅ Embedding generated successfully!")
    print(f"Vector length: {len(embedding)}")
    print("\nFirst 10 values:")
    print(embedding[:10])

except Exception as e:
    print("❌ Error:")
    print(e)