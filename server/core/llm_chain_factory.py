from config.settings import GROQ_API_KEY, GOOGLE_API_KEY

from langchain_core.prompts import ChatPromptTemplate

from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain
)

from langchain_classic.chains.retrieval import (
    create_retrieval_chain
)

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from utils.logger import logger


def get_prompt():
    logger.debug("Creating chat prompt template.")

    return ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are a helpful PDF question-answering assistant.

Use only the provided context to answer the user's question.
If the answer is not available in the context, say:
"I don't know based on the provided documents."

Do not make assumptions or add information from outside the documents.
If the context is partially relevant, answer only with the available information and mention that the documents do not provide complete details.

Give clear, simple, and well-structured answers.
"""
        ),
        (
            "human",
            "Context:\n{context}\n\nQuestion:\n{input}"
        )
    ])


def get_llm(model_provider: str, model: str):
    logger.debug(f"Initializing LLM for {model_provider} - {model}")

    if model_provider == "groq":
        return ChatGroq(
            model=model,
            api_key=GROQ_API_KEY
        )

    elif model_provider == "gemini":
        return ChatGoogleGenerativeAI(
            model=model,
            api_key=GOOGLE_API_KEY
        )

    else:
        logger.error(f"Unsupported LLM Provider: {model_provider}")
        raise ValueError(f"Unsupported LLM Provider: {model_provider}")


def build_llm_chain(model_provider: str, model: str, retriever):
    logger.debug(
        f"Building LLM chain for provider: {model_provider}, model: {model}"
    )

    prompt = get_prompt()
    llm = get_llm(model_provider, model)

    document_chain = create_stuff_documents_chain(
        llm,
        prompt
    )

    retrieval_chain = create_retrieval_chain(
        retriever,
        document_chain
    )

    return retrieval_chain