import ollama

response = ollama.embed(
    model="nomic-embed-text",
    input="Hello world"
)

print(len(response["embeddings"][0]))
print("Embedding works!")