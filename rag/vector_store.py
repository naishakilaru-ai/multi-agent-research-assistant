import chromadb

# Create a persistent ChromaDB client
client = chromadb.PersistentClient(path="./database")

# Create or load a collection
collection = client.get_or_create_collection(
    name="research_documents"
)


def add_document(doc_id, text, embedding, metadata):
    """
    Store a document and its embedding in ChromaDB.
    """

    collection.add(
        ids=[doc_id],
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata]
    )


def search(query_embedding, n_results=3,document=None):
    """
    Search for the most similar documents.
    """
    if document:

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where={"source": document},
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

    else:

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=[
            "documents",
            "metadatas",
            "distances"
            ]
        )

    return results

def get_all_documents():
    """
    Returns every stored document chunk.
    """

    return collection.get(
        include=[
            "documents",
            "metadatas"
        ]
    )
def get_documents_by_file(filename):
    """
    Return only the chunks belonging to one PDF.
    """

    results = collection.get(
        include=[
            "documents",
            "metadatas"
        ]
    )

    documents = []
    metadatas = []

    for doc, meta in zip(results["documents"], results["metadatas"]):

        if meta["source"] == filename:
            documents.append(doc)
            metadatas.append(meta)

    return {
        "documents": documents,
        "metadatas": metadatas
    }
def get_uploaded_documents():
    """
    Return a list of unique uploaded PDF filenames.
    """

    results = collection.get(
        include=["metadatas"]
    )

    files = set()

    for metadata in results["metadatas"]:
        files.add(metadata["source"])

    return sorted(list(files))