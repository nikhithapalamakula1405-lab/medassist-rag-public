import os
import json
import math
import sqlite3

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY"),
    http_options=types.HttpOptions(timeout=30000)
)

def cosine_similarity(vector1, vector2):
    dot = sum(a * b for a, b in zip(vector1, vector2))
    mag1 = math.sqrt(sum(a * a for a in vector1))
    mag2 = math.sqrt(sum(b * b for b in vector2))

    if mag1 == 0 or mag2 == 0:
        return 0

    return dot / (mag1 * mag2)


question = input("Ask MediAssist: ")

print("Creating question embedding...", flush=True)

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=question
)

question_embedding = response.embeddings[0].values

connection = sqlite3.connect("mediassist.db")
cursor = connection.cursor()

cursor.execute("SELECT text, embedding FROM healthcare_vectors")
records = cursor.fetchall()

if not records:
    print("No healthcare documents found in database.")
    connection.close()
    raise SystemExit

results = []

for text, embedding_json in records:
    stored_embedding = json.loads(embedding_json)
    score = cosine_similarity(question_embedding, stored_embedding)
    results.append((score, text))

results.sort(key=lambda item: item[0], reverse=True)

top_results = results[:8]

context = "\n\n".join(item[1] for item in top_results)

print("\nRetrieved Context:\n")
print(context)

prompt = f"""
You are MediAssist, a healthcare information assistant.

Answer the user's question using only the context below.
If the answer is not available in the context, say:
"I could not find this information in the provided healthcare document."

Do not invent information.

Context:
{context}

Question:
{question}

Answer:
"""

print("Generating answer from Gemini...", flush=True)

try:
    answer = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    print("\nMediAssist Answer:\n")
    print(answer.text)

except Exception as error:
    print("\nGemini Error:", error)

finally:
    connection.close()