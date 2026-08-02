import os

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.embeddings import get_embedding
from rag.vector_store import add_document


def ingest_pdf(pdf_path):
    """
    Reads a PDF, splits it into chunks,
    generates embeddings, and stores them in ChromaDB.
    """

    print("=" * 50)
    print("Starting PDF ingestion...")

    # Read PDF
    reader = PdfReader(pdf_path)

    # Get filename
    pdf_name = os.path.basename(pdf_path)

    print(f"PDF Name: {pdf_name}")
    print(f"Total Pages: {len(reader.pages)}")

    # Text splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    total_chunks = 0

    # Process page by page
    for page_number, page in enumerate(reader.pages, start=1):

        print(f"\nProcessing Page {page_number}")

        page_text = page.extract_text()

        if not page_text:
            print("No text found on this page. Skipping...")
            continue

        chunks = splitter.split_text(page_text)

        print(f"Chunks on page {page_number}: {len(chunks)}")

        for i, chunk in enumerate(chunks):

            print(f"Generating embedding for chunk {i}...")

            embedding = get_embedding(chunk)

            print("Embedding generated.")

            add_document(
                doc_id=f"{pdf_name}_page{page_number}_chunk{i}",
                text=chunk,
                embedding=embedding,
                metadata={
                    "source": pdf_name,
                    "page": page_number
                }
            )

            print(f"✅ Stored chunk {i} from page {page_number}")
            total_chunks += 1

    print("\n" + "=" * 50)
    print(f"Total chunks stored: {total_chunks}")
    print("PDF successfully stored in ChromaDB.")
    print("=" * 50)