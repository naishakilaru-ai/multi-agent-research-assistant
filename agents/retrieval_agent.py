from rag.embeddings import get_embedding
from rag.vector_store import search


def retrieve_context(question: str, document: str | None = None):
    """
    Retrieves relevant document chunks
    for a user's question from a single document.
    """

    query_embedding = get_embedding(question)

    results = search(
        query_embedding=query_embedding,
        n_results=5,
        document=document
    )

    return results


def retrieve_multiple_context(question: str, documents: list[str]):
    """
    Retrieves relevant chunks from multiple selected documents.
    """

    query_embedding = get_embedding(question)

    all_documents = []
    all_metadatas = []

    for doc in documents:

        results = search(
            query_embedding=query_embedding,
            n_results=5,
            document=doc
        )
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        for chunk in docs:
            all_documents.append(chunk)
        for meta in metas:
            all_metadatas.append(meta)

    return {
        "documents": [all_documents],
        "metadatas": [all_metadatas]
    }