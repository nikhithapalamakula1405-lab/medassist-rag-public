import streamlit as st
import os
import json
import math
import sqlite3

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

st.set_page_config(page_title="MediAssist AI", page_icon="🏥")

st.title("🏥 MediAssist AI")
st.subheader("Your Healthcare Document Assistant")
st.info("Ask questions based on the GE HealthCare Sustainability Report.")

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Google API key not found. Check your .env file.")
    st.stop()

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=30000)
)

def cosine_similarity(v1, v2):
    dot = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))

    if mag1 == 0 or mag2 == 0:
        return 0

    return dot / (mag1 * mag2)


def get_answer(question):

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=question
    )

    question_embedding = response.embeddings[0].values

    connection = sqlite3.connect("mediassist.db")
    cursor = connection.cursor()

    cursor.execute("SELECT text, embedding FROM healthcare_vectors")
    records = cursor.fetchall()
    connection.close()

    if not records:
        return "No documents found in the database."

    results = []

    for text, embedding_json in records:
        stored_embedding = json.loads(embedding_json)
        score = cosine_similarity(question_embedding, stored_embedding)
        results.append((score, text))

    results.sort(key=lambda item: item[0], reverse=True)

    context = "\n\n".join(item[1] for item in results[:8])

    prompt = f"""
    You are MediAssist, a healthcare document assistant.
    Answer using only the provided context.
    If information is unavailable, say so.
    Do not invent facts or provide medical diagnoses.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    answer = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return answer.text


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask your healthcare question...")

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("MediAssist is preparing your answer..."):

            try:
                answer = get_answer(question)
                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"Error: {e}")

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.divider()
st.caption("MediAssist AI | RAG-Based Healthcare Document Assistant")
st.caption("For informational purposes only. Not a substitute for professional medical advice.")