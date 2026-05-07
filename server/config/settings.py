import os
from dotenv import load_dotenv


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

TEMPFILE_UPLOAD_DIRECTORY = "./temp/uploaded_files"

MODEL_OPTIONS = {
    "groq": {
        "playground": "https://console.groq.com",
        "models": [
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile"
        ]
    },
    "gemini": {
        "playground": "https://ai.google.dev",
        "models": [
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite",
            "gemini-2.5-pro"
        ]
    }
}

VECTORSTORE_DIRECTORY = {
    key.lower(): f"./data/{key.lower()}_vector_store"
    for key in MODEL_OPTIONS.keys()
}

KNOWLEDGE_BASE_DIRECTORY = "./data/knowledge_base"

KNOWLEDGE_BASE_VECTORSTORE = "./data/knowledge_base_vectorstore"