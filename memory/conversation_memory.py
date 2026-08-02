conversation_history = []


def add_to_memory(question, answer):
    """
    Store the latest conversation.
    """

    conversation_history.append({
        "question": question,
        "answer": answer
    })

    # Keep only last 5 conversations
    if len(conversation_history) > 5:
        conversation_history.pop(0)


def get_memory():

    memory = ""

    for item in conversation_history:

        memory += f"""
User:
{item['question']}

Assistant:
{item['answer']}

"""

    return memory