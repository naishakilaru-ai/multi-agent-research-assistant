from agents.summary_agent import summarize

context = """
Artificial Intelligence is the simulation
of human intelligence by machines.

AI includes machine learning,
deep learning and NLP.
"""

question = "What is Artificial Intelligence?"

answer = summarize(question, context)

print(answer)