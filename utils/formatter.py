import re


def format_answer(answer: str) -> str:
    """
    Format the LLM response into clean Markdown.
    """

    # Remove extra spaces
    answer = answer.strip()

    # Ensure headings start on a new line
    answer = re.sub(r"(### .+)", r"\n\1\n", answer)

    # Ensure bullets start on new lines
    answer = re.sub(r"- ", r"\n- ", answer)

    # Remove multiple blank lines
    answer = re.sub(r"\n{3,}", "\n\n", answer)

    return answer.strip()