# 🧠 DocuMind AI

RAG-based AI chatbot using FastAPI, Streamlit, LangChain, and ChromaDB with support for:

- 📚 Preloaded Knowledge Base PDFs
- 📄 User-uploaded PDFs
- ⚡ Groq & Gemini LLMs
- 🔍 Retrieval Augmented Generation (RAG)

---

# 🚀 Features

- Chat with PDFs
- Persistent Knowledge Base
- User PDF Uploads
- FastAPI Backend
- Streamlit Frontend
- Chroma Vector Database
- Multi-LLM Support
- Knowledge Base + Uploaded PDF Retrieval
- Modern AI Chat Interface

---

# 📦 Project Setup

## 1️⃣ Clone Repository

```bash
git clone <https://github.com/ASAShh/DocuMind-AI>
cd RAG-BOT-FASTAPI-MAIN
```

---

# 🐍 Create Virtual Environment

## Windows

```bash
python -m venv .venv
```

Activate virtual environment:

```bash
.venv\Scripts\activate
```

---

## Linux / Mac

```bash
python3 -m venv .venv
```

Activate virtual environment:

```bash
source .venv/bin/activate
```

---

# 📥 Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file inside the `server/` directory.

## File

```text
server/.env
```

## Add

```env
GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
```

---

# 📚 Knowledge Base Setup

Place your permanent knowledge base PDFs inside:

```text
server/data/knowledge_base/
```

These PDFs are indexed once and reused across sessions.

---

# 🧠 Embedding Models

The project uses different embedding models depending on the selected AI provider.

| Provider | Embedding Model |
|---|---|
| Groq | `sentence-transformers/all-MiniLM-L12-v2` |
| Gemini | `models/embedding-001` |

## Why These Models?

### `sentence-transformers/all-MiniLM-L12-v2`
- Lightweight and fast
- Good semantic similarity performance
- Efficient for local vector embeddings

### `models/embedding-001`
- Google's semantic embedding model
- Optimized for Gemini ecosystem
- Good contextual understanding for RAG pipelines

These embedding models convert document text into vector representations stored in ChromaDB for semantic similarity search.

---

# ⚠️ Important

Activate the virtual environment separately in each terminal before running the backend and frontend.

---

# ▶️ Run Backend Server

## Terminal 1

```bash
.venv\Scripts\activate
cd server
uvicorn main:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

---

# 💬 Run Frontend

## Terminal 2

```bash
.venv\Scripts\activate
cd client
streamlit run app.py
```

Frontend runs on:

```text
http://localhost:8501
```

---

# 📂 Project Structure

```text
RAG-BOT-FASTAPI-MAIN/
│
├── client/
│   ├── components/
│   │   ├── chat.py
│   │   ├── sidebar.py
│   │
│   ├── state/
│   │   ├── session.py
│   │
│   ├── utils/
│   │   ├── api.py
│   │   ├── config.py
│   │   ├── helpers.py
│   │
│   ├── app.py
│
├── server/
│   ├── api/
│   │   ├── routes.py
│   │   ├── schemas.py
│   │
│   ├── config/
│   │   ├── settings.py
│   │
│   ├── core/
│   │   ├── document_processor.py
│   │   ├── llm_chain_factory.py
│   │   ├── vector_database.py
│   │
│   ├── data/
│   │   ├── knowledge_base/
│   │
│   ├── utils/
│   │   ├── logger.py
│   │
│   ├── main.py
│
├── requirements.txt
├── pyproject.toml
├── README.md
```

---

# ⚡ Tech Stack

- Streamlit
- FastAPI
- LangChain
- ChromaDB
- Groq
- Gemini
- HuggingFace Embeddings

---

# 👨‍💻 Author

Ashwin Bhatt