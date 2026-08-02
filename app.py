import os
import shutil
from utils.formatter import format_answer
from collections import defaultdict


from fastapi import FastAPI, Request, UploadFile, File, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from memory.conversation_memory import add_to_memory
from agents.query_rewriter import rewrite_query
from memory.conversation_memory import get_memory, add_to_memory
from agents.retrieval_agent import (
    retrieve_context,
    retrieve_multiple_context
)

from rag.ingest import ingest_pdf
import current_document
from pydantic import BaseModel

from agents.summary_agent import summarize
from agents.learning_agent import save_interaction
from agents.pdf_summary_agent import (
    summarize_batch,
    summarize_document
)
from rag.vector_store import (
    get_documents_by_file,
    get_uploaded_documents
)

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str
    documents: list[str] = []

# ==========================
# Static Files
# ==========================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

# ==========================
# Templates
# ==========================

templates = Jinja2Templates(
    directory="templates"
)

# ==========================
# Upload Folder
# ==========================

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# ==========================
# Home Page
# ==========================

@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

# ==========================
# Background PDF Ingestion
# ==========================

def process_pdf(file_path: str):

    print("Starting background ingestion...")

    ingest_pdf(file_path)

    print("Background ingestion completed.")

# ==========================
# Upload PDF
# ==========================

@app.post("/upload")
async def upload_file(background_tasks: BackgroundTasks,file: UploadFile = File(...)):

    try:

        print("=" * 60)
        print("1. Upload request received")

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )
        current_document.CURRENT_DOCUMENT = file.filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("2. File saved:", file_path)

        background_tasks.add_task(
        process_pdf,
        file_path
        )

        print("3. Ingestion complete")

        print("=" * 60)

        return {
            "message": "Upload successful. Document is being processed.",
            "filename": file.filename
        }

    except Exception as e:

        print("\nUPLOAD FAILED")
        print(type(e).__name__)
        print(e)

        return {
            "error": str(e)
        }
    # ==========================
# Ask Question
# ==========================
@app.post("/ask")
async def ask_question(request: QuestionRequest):
    print("Received request:", request)
    print("Selected documents:", request.documents)
    import traceback
    try:

        # Retrieve relevant chunks
        history=get_memory()
        search_query=rewrite_query(
            request.question,
            history
        )

        selected_documents=request.documents
        if len(selected_documents) == 0:
            selected_documents = [current_document.CURRENT_DOCUMENT]
        question_lower = request.question.lower()
        is_multi_summary = (
                len(selected_documents) > 1 and
                (
                    "summarize both" in question_lower or
                    "summarise both" in question_lower or
                    "summarize all" in question_lower or
                    "summarise all" in question_lower or
                    "summarize selected" in question_lower or
                    "summarise selected" in question_lower
                )
            )
        if len(selected_documents) == 1:
            results = retrieve_context(search_query,selected_documents[0])
            
        else:
            results = retrieve_multiple_context(search_query,selected_documents)

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        unique_documents = []
        unique_metadatas = []
        seen = set()
        for doc, meta in zip(documents, metadatas):
            if doc not in seen:
                seen.add(doc)
                unique_documents.append(doc)
                unique_metadatas.append(meta)
        documents = unique_documents
        metadatas = unique_metadatas

        if len(documents) == 0:

            return {
                "answer": "No relevant information found.",
                "sources": []
            }
        print(documents)
        print(type(documents))
        print(type(documents[0]))

        # Build context
        grouped = defaultdict(list)
        for doc, meta in zip(documents, metadatas):
            grouped[meta["source"]].append(doc)
        context = ""
        for filename, chunks in grouped.items():
            context += f"\n\n===== Document: {filename} =====\n"
            context += "\n\n".join(chunks)

        # Build sources
        sources = []

        for metadata in metadatas:

            sources.append({
                "file": metadata["source"],
                "page": metadata["page"]
            })

        if is_multi_summary:
            summaries = []
            grouped = defaultdict(list)
            for doc, meta in zip(documents, metadatas):
                grouped[meta["source"]].append(doc)
            for filename, chunks in grouped.items():
                document_context = "\n\n".join(chunks)
                document_summary = summarize(
                    f"Summarize this paper only: {filename}",
                    document_context
                )
                summaries.append(
                    f"## 📄 {filename}\n\n{document_summary}"
                )
            answer = "\n\n---\n\n".join(summaries)
        else:
            answer = summarize(
                request.question,
                context
            )
        answer=format_answer(answer)
            

        save_interaction(
            request.question,
            answer,
            sources
        )
        add_to_memory(
        request.question,
        answer
        )
        return{
            "answer": answer,
            "sources": sources
        }

        

    except Exception as e:

        traceback.print_exc()

        return {
            "answer": "Internal server error",
            "sources": []
        }
    
    
    # ==========================
# Summarize Entire PDF
# ==========================

@app.get("/summarize")
async def summarize_pdf():

    try:

        # Get all document chunks
        results = get_documents_by_file(
        current_document.CURRENT_DOCUMENT
        )

        documents = results["documents"]

        print(f"Total Chunks: {len(documents)}")

        if not documents:

            return {
                "summary": "No document has been uploaded."
            }

        print(f"Total Chunks: {len(documents)}")

        batch_size = 20
        batch_summaries = []

        # Process chunks in batches
        for i in range(0, len(documents), batch_size):

            batch = documents[i:i + batch_size]

            batch_number = (i // batch_size) + 1
            total_batches = (len(documents) + batch_size - 1) // batch_size

            print(f"Summarizing batch {batch_number}/{total_batches}")

            summary = summarize_batch(batch)

            batch_summaries.append(summary)

        # Combine batch summaries
        combined_summary = "\n\n".join(batch_summaries)

        print("Generating final structured summary...")

        final_summary = summarize_document(combined_summary)

        return {
            "summary": final_summary
        }

    except Exception as e:

        print("SUMMARY ERROR:", e)

        return {
            "summary": str(e)
        }
# ==========================
# List Uploaded Documents
# ==========================

@app.get("/documents")
async def list_documents():

    try:

        documents = get_uploaded_documents()

        return {
            "documents": documents
        }

    except Exception as e:

        return {
            "documents": [],
            "error": str(e)
        }