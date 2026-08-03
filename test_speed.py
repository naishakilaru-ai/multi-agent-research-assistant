import time
from llm.gemini import generate_response

start = time.time()

response = generate_response("Say hello in one sentence.")

print(response)

print("Time:", time.time() - start, "seconds")