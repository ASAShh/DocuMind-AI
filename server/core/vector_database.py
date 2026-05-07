import os

from typing import List
from fastapi import UploadFile

from config.settings import (
  GOOGLE_API_KEY,
  VECTORSTORE_DIRECTORY,
  MODEL_OPTIONS,
  KNOWLEDGE_BASE_DIRECTORY,
  KNOWLEDGE_BASE_VECTORSTORE
)
from core.document_processor import (
    save_uploaded_file,
    load_documents_from_paths,
    split_documents_to_chunks
)
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from utils.logger import logger


def vectorstore_exists(persist_path: str) -> bool:
  exists = os.path.exists(persist_path) and bool(os.listdir(persist_path))
  logger.debug(f"Vectorstore exists at {persist_path}: {exists}")
  return exists

def get_embeddings(model_provider: str):
  logger.debug(f"Getting embeddings for provider: {model_provider}")

  if model_provider in ["groq", "gemini"]:
    return HuggingFaceEmbeddings(
      model_name="sentence-transformers/all-MiniLM-L12-v2"
    )

  logger.error(f"Unsupported LLM Provider: {model_provider}")
  raise ValueError(f"Unsupported LLM Provider: {model_provider}")

def initialize_empty_vectorstores():
  logger.info("Initializing empty vectorstores...")
  for provider in MODEL_OPTIONS.keys():
    persist_path = VECTORSTORE_DIRECTORY[provider]
    os.makedirs(persist_path, exist_ok=True)

    if not os.listdir(persist_path):
      embedding = get_embeddings(provider)
      Chroma(
        embedding_function=embedding,
        persist_directory=persist_path
      )
      logger.debug(f"Initialized vectorstore for {provider} at {persist_path}")

  logger.info("Vectorstore initialization complete.")

async def upsert_vectorstore_from_pdfs(uploaded_files: List[UploadFile], model_provider: str):
  logger.debug(f"Upserting vectorstore for {model_provider}")
  file_paths = await save_uploaded_file(uploaded_files)
  docs = load_documents_from_paths(file_paths)
  chunks = split_documents_to_chunks(docs)
  embedding = get_embeddings(model_provider)

  persist_path = VECTORSTORE_DIRECTORY[model_provider]

  if vectorstore_exists(persist_path):
    logger.debug("Appending to existing vectorstore...")
    vectorstore = Chroma(persist_directory=persist_path, embedding_function=embedding)
    vectorstore.add_documents(chunks)
    logger.debug(f"Added {len(chunks)} chunks to existing vectorstore.")
  else:
    vectorstore = Chroma.from_documents(documents=chunks, embedding=embedding, persist_directory=persist_path)
    logger.debug(f"Created new vectorstore with {len(chunks)} chunks.")

  return vectorstore

def load_vectorstore(model_provider: str):
  persist_path = VECTORSTORE_DIRECTORY[model_provider]
  logger.debug(f"Loading vectorstore from {persist_path}")

  if vectorstore_exists(persist_path):
    logger.debug(f"Loading existing vectorstore for provider: {model_provider}")
    return Chroma(persist_directory=persist_path, embedding_function=get_embeddings(model_provider))

  logger.debug(f"VectorStore not found for provider: {model_provider}")
  raise ValueError(f"VectorStore not found for provider: {model_provider}")

def get_knowledge_base_pdf_paths():
  kb_dir = KNOWLEDGE_BASE_DIRECTORY

  os.makedirs(kb_dir, exist_ok=True)

  return [
    os.path.join(kb_dir, file)
    for file in os.listdir(kb_dir)
    if file.endswith(".pdf")
  ]

def initialize_knowledge_base(model_provider: str):
  logger.info(f"Initializing knowledge base for {model_provider}")

  embedding = get_embeddings(model_provider)

  persist_path = f"{KNOWLEDGE_BASE_VECTORSTORE}_{model_provider}"

  os.makedirs(persist_path, exist_ok=True)

  vectorstore = Chroma(
    persist_directory=persist_path,
    embedding_function=embedding
  )

  existing_sources = set()

  try:
    existing_docs = vectorstore.get()

    if existing_docs and "metadatas" in existing_docs:
      for metadata in existing_docs["metadatas"]:
        if metadata and metadata.get("source"):
          existing_sources.add(metadata["source"])


  except Exception as e:

    logger.warning(f"Could not read existing knowledge base metadata: {str(e)}")

  pdf_paths = get_knowledge_base_pdf_paths()

  new_pdf_paths = [
    path for path in pdf_paths
    if path not in existing_sources
  ]

  if not new_pdf_paths:
    logger.info("No new KB PDFs found.")
    return

  logger.info(f"Processing {len(new_pdf_paths)} new KB PDFs")

  docs = load_documents_from_paths(new_pdf_paths)

  chunks = split_documents_to_chunks(docs)

  vectorstore.add_documents(chunks)

  logger.info("Knowledge base updated.")