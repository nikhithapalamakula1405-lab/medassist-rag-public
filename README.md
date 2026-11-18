# 🏥 MediAssist AI – RAG-Based Healthcare Document Assistant

An AI-powered healthcare document assistant built using Python, Streamlit, Google's Gemini AI, and Retrieval-Augmented Generation (RAG).

## 📌 Project Overview

MediAssist AI helps users understand healthcare documents and find relevant information by asking questions in natural language.

The application uses RAG technology to retrieve relevant document information and generate AI-powered responses.

## 🚀 Key Features

- Healthcare PDF document processing.
- AI-powered question answering.
- Retrieval-Augmented Generation (RAG).
- Semantic search using vector embeddings.
- Google Gemini AI integration.
- Interactive Streamlit interface.
- Context-based responses.

## 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini AI
- LangChain
- Hugging Face
- FAISS
- PyPDF
- SQLite

## 📂 Project Structure

```text
medassist-rag-public/
│
├── app.py
├── rag_pipeline.py
├── retriever.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the project directory

```bash
cd medassist-rag-public
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Google API Key

Create a `.env` file in the project directory.

Add:

```env
GOOGLE_API_KEY=your_google_api_key
```

Never upload your API key to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

## 🔐 Security

- API keys are stored in environment variables.
- Sensitive credentials should never be committed to GitHub.
- Healthcare information should be handled responsibly.

## ⚠️ Disclaimer

MediAssist AI is an educational AI project. It is not a replacement for professional medical advice, diagnosis, or treatment.

## 👨‍💻 Author

Developed as an AI-powered healthcare document assistant project.