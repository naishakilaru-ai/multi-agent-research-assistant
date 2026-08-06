# Multi-Agent Research Assistant

An AI-powered research assistant that allows users to upload research papers (PDFs), ask questions in natural language, generate summaries, and retrieve relevant information using Retrieval-Augmented Generation (RAG).

Built using **FastAPI**, **Ollama**, **ChromaDB**, and **Sentence Transformers**, the application employs a **multi-agent architecture** to process user queries efficiently.

---

##  Features

-  Upload one or multiple research papers (PDF)
-  Multi-Agent Architecture
  - Query Rewriting Agent
  - Retrieval Agent
  - Summary Agent
  - Learning Agent
-  Retrieval-Augmented Generation (RAG)
-  Semantic search using Sentence Transformers
-  ChromaDB vector database
-  Conversational memory for follow-up questions
-  Multi-document question answering
-  Complete paper summarization
-  Source attribution with page numbers
-  Modern and responsive user interface

---

##  System Architecture

```
                User
                  │
                  ▼
         Upload Research Papers
                  │
                  ▼
          PDF Processing Agent
                  │
                  ▼
      Chunking + Embedding Generation
                  │
                  ▼
             ChromaDB Storage
                  │
                  ▼
──────────────────────────────────────────

User Question
      │
      ▼
Query Rewriting Agent
      │
      ▼
Retrieval Agent
      │
      ▼
Relevant Context
      │
      ▼
Summary Agent (LLM)
      │
      ▼
Formatted Response
      │
      ▼
Conversation Memory
```

---

#  Tech Stack

### Backend

- FastAPI
- Python

### AI & NLP

- Ollama
- Sentence Transformers
- RAG Pipeline

### Vector Database

- ChromaDB

### Frontend

- HTML
- CSS
- JavaScript

### PDF Processing

- PyPDF
- LangChain Text Splitters

---

#  Project Structure

```
Multi-Agent-Research-Assistant/
│
├── agents/
│   ├── learning_agent.py
│   ├── pdf_summary_agent.py
│   ├── query_rewriter.py
│   ├── retrieval_agent.py
│   └── summary_agent.py
│
├── rag/
│   ├── embeddings.py
│   ├── ingest.py
│   └── vector_store.py
│
├── memory/
│
├── static/
│
├── templates/
│
├── uploads/
│
├── utils/
│
├── app.py
├── config.py
├── current_document.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/naishakilaru-ai/multi-agent-research-assistant.git

cd multi-agent-research-assistant
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Start Ollama

Ensure Ollama is installed and running.

Example:

```bash
ollama run llama3.2
```

---

## Run Application

```bash
python -m uvicorn app:app --reload
```

Open:

```
http://127.0.0.1:8000
```

---

#  Usage

1. Upload one or more research papers.
2. Select the papers you want to query.
3. Ask questions in natural language.
4. View AI-generated answers with sources.
5. Generate summaries of uploaded papers.

---

#  Screenshots

> Add screenshots here after uploading them.

Example:

```
screenshots/
├── home.png
├── upload.png
├── chat.png
├── summary.png
```

---

#  Example Questions

### Single Paper

- What is the paper about?
- Summarize this paper.
- What methodology was used?
- What are the limitations?
- What are the key findings?

### Multiple Papers

- Compare these papers.
- What are the common themes?
- Summarize both papers.
- Which paper discusses blockchain?
- Which paper focuses on climate change?

---

#  Key Highlights

- Multi-Agent workflow
- Retrieval-Augmented Generation (RAG)
- Semantic document search
- Conversational memory
- Multi-document retrieval
- Source-aware responses
- Modular architecture
- Interactive research assistant interface

---

# 🔮 Future Improvements

- PDF citation export
- Research paper comparison tables
- Streaming responses
- User authentication
- Cloud deployment
- Research note generation
- Keyword extraction
- Reference management

---

#  Author

**Naisha Kilaru**

GitHub: https://github.com/naishakilaru-ai

---

# ⭐ If you found this project useful, consider giving it a star!
