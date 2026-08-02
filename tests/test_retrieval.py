from agents.retrieval_agent import retrieve_context

question = input("Ask a question: ")

results = retrieve_context(question)

print("\nTop Retrieved Chunks:\n")

documents = results["documents"][0]
metadatas = results["metadatas"][0]
distances = results["distances"][0]

for i in range(len(documents)):
    print("=" * 60)
    print(f"Result {i+1}")
    print(f"Source : {metadatas[i]['source']}")
    print(f"Page   : {metadatas[i]['page']}")
    print(f"Distance : {distances[i]:.4f}")
    print()
    print(documents[i])
    print()