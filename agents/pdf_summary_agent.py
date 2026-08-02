import ollama
from config import OLLAMA_MODEL


MODEL = OLLAMA_MODEL


def summarize_chunk(chunk: str):
    """
    Summarize one chunk of a research paper.
    """

    prompt = f"""
You are an expert research paper analyst.

Summarize the following section of a research paper.

Focus ONLY on the important information.

Include, if present:
- Main idea
- Methodology
- Important findings
- Experimental results
- Contributions

Keep the summary concise (3–6 sentences).

Research Paper Section:

{chunk}
"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
        "num_predict": 300,
        "temperature": 0.2
        }
    )

    return response["message"]["content"]

def summarize_batch(chunks: list[str]):
    """
    Summarize a batch of document chunks together.
    """

    combined_text = "\n\n".join(chunks)

    prompt = f"""
You are an expert research paper analyst.

Summarize the following sections of a research paper.

Focus on:

- Main objective
- Methodology
- Important findings
- Results
- Contributions

Keep the summary concise but complete.

Research Paper Sections:

{combined_text}
"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
        "num_predict": 300,
        "temperature": 0.2
        }
    )

    return response["message"]["content"]


def summarize_document(chunk_summaries: str):
    """
    Combine all chunk summaries into one
    professional research paper summary.
    """

    prompt = f"""
You are an expert research assistant.

Using the research paper summaries below,
generate a professional structured summary.

Follow EXACTLY this format.

# 📄 Paper Overview
Write a short overview of the paper in 2–3 sentences.

# 🎯 Objective
Explain the main objective or research problem.

# 📚 Background
Briefly explain the motivation or context.

# 🔬 Methodology
Describe the proposed method or approach.

# 📊 Results
Summarize the important experimental or evaluation results.

# 💡 Key Contributions
List the major contributions as bullet points.

# ⚠️ Limitations
Mention the limitations if available.
If none are mentioned, write:
"Not explicitly discussed in the paper."

# 🚀 Future Work
Mention future research directions if available.
If none are mentioned, write:
"Not explicitly discussed in the paper."

# ✅ Conclusion
Write a concise conclusion in 2–3 sentences.

Research Paper Summaries:

{chunk_summaries}
"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
        "num_predict": 300,
        "temperature": 0.2
        }
    )

    return response["message"]["content"]