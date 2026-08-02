import ollama
from config import OLLAMA_MODEL
from memory.conversation_memory import get_memory

def summarize(question: str, context: str):
    memory = get_memory()
    prompt = f"""
You are an intelligent research assistant.

Use the document context as the primary source of truth.

The context may contain one or more research papers.
Each paper is separated using:

===== Document: filename =====

You may rephrase, simplify, summarize, or explain the information in simpler terms when it improves understanding.

If multiple documents are provided:
- Read information from ALL selected documents before answering.
- If the user asks to summarize multiple papers, summarize each paper separately.
- If the user asks to compare papers, compare them clearly.
- Do not mix information from different papers.
- Mention the document names whenever appropriate.

If only one document is relevant, answer only from that document.

If the document context does not contain enough information to answer the question, reply exactly:
"I could not find enough information in the uploaded document(s)."

Instructions:
- Format the answer using valid Markdown.
- Leave one blank line after every heading.
- Leave one blank line before and after every bullet list.
- Each bullet point must be on its own line.
- Do not write multiple bullet points on the same line.
- Keep the answer concise and easy to read.
- Highlight important terms using **bold**.

Use this exact format:

### ✅ Answer

- Point 1
- Point 2
- Point 3

### 💡 Simple Explanation

Explain in 2–3 simple sentences.

### 📌 Key Takeaways

- Takeaway 1
- Takeaway 2
- Takeaway 3

Document Context:
{context}

Question:
{question}

Answer:
"""

    response = ollama.chat(
    model=OLLAMA_MODEL,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)
    print("\n========== RAW MODEL OUTPUT ==========")
    print(response["message"]["content"])
    print("======================================\n")
    
    return response["message"]["content"]