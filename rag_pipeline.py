import os
import json
import sqlite3
from pypdf import PdfReader
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Connect to Gemini
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

# Step 1: Load PDF
pdf_path = "data/healthcare_guide.pdf"

reader = PdfReader(pdf_path)

text = ""

for page in reader.pages:
    text += page.extract_text() or ""

print("PDF loaded successfully!")

# Step 2: Split text into chunks
chunk_size = 1000
overlap = 200

chunks = []

for i in range(0, len(text), chunk_size - overlap):
    chunk = text[i:i + chunk_size]

    if chunk.strip():
        chunks.append(chunk)

print("Total chunks:", len(chunks))

# Step 3: Create SQLite database
connection = sqlite3.connect("mediassist.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS healthcare_vectors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    embedding TEXT
)
""")

# Clear previous records before inserting again
cursor.execute("DELETE FROM healthcare_vectors")

# Step 4: Generate and store embeddings
for start in range(0, len(chunks), 50):

    batch = chunks[start:start + 50]

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=batch
    )

    for chunk, embedding in zip(batch, response.embeddings):

        cursor.execute(
            "INSERT INTO healthcare_vectors (text, embedding) VALUES (?, ?)",
            (chunk, json.dumps(embedding.values))
        )

    connection.commit()

    print("Processed chunks:", min(start + 50, len(chunks)), "/", len(chunks))

connection.close()

print("\nAll healthcare embeddings stored successfully!")