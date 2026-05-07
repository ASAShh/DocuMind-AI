from fastapi import APIRouter, UploadFile, File, Form

from config.settings import (
    MODEL_OPTIONS,
    KNOWLEDGE_BASE_VECTORSTORE
)

from core.vector_database import (
    upsert_vectorstore_from_pdfs,
    load_vectorstore,
    get_embeddings
)

from core.llm_chain_factory import build_llm_chain

from api.schemas import (
    ChatRequest,
    StandardAPIResponse
)

from utils.logger import logger

from langchain_classic.retrievers import MergerRetriever
from langchain_community.vectorstores import Chroma


router = APIRouter()


@router.get("/health", response_model=StandardAPIResponse)
def health_check():
    logger.debug("Health check requested")

    return StandardAPIResponse(
        status="success",
        data="ok",
        message="Service is healthy"
    )


@router.get("/llm", response_model=StandardAPIResponse)
async def get_llm_options():
    logger.debug("Fetching LLM providers.")

    return StandardAPIResponse(
        status="success",
        data=[provider.title() for provider in MODEL_OPTIONS.keys()]
    )


@router.get("/llm/{model_provider}", response_model=StandardAPIResponse)
async def get_llm_models(model_provider: str):

    model_provider = model_provider.lower()

    if model_provider not in MODEL_OPTIONS:
        logger.warning(f"Invalid model provider: {model_provider}")

        return StandardAPIResponse(
            status="error",
            message="Invalid model provider."
        )

    logger.debug(f"Fetching models for provider: {model_provider}")

    return StandardAPIResponse(
        status="success",
        data=MODEL_OPTIONS[model_provider]["models"]
    )


@router.post("/upload_and_process_pdfs", response_model=StandardAPIResponse)
async def upload_and_process_pdfs(
    files: list[UploadFile] = File(...),
    model_provider: str = Form(...)
):

    try:
        model_provider = model_provider.lower()

        logger.info(
            f"Received {len(files)} files for model provider: {model_provider}"
        )

        await upsert_vectorstore_from_pdfs(
            files,
            model_provider
        )

        logger.info("Files processed successfully")

        return StandardAPIResponse(
            status="success",
            data="PDFs processed successfully."
        )

    except Exception as e:

        logger.exception("Error while uploading and processing files")

        return StandardAPIResponse(
            status="error",
            message=str(e)
        )


@router.post("/chat", response_model=StandardAPIResponse)
async def chat(request: ChatRequest):

    try:
        message = request.message
        model_name = request.model_name
        model_provider = request.model_provider.lower()

        logger.debug(
            f"Chat request for model: {model_name} "
            f"(provider: {model_provider})"
        )

        if model_provider not in MODEL_OPTIONS:

            logger.warning("Invalid model provider.")

            return StandardAPIResponse(
                status="error",
                message="Invalid model provider."
            )

        if model_name not in MODEL_OPTIONS[model_provider]["models"]:

            logger.warning("Invalid model name.")

            return StandardAPIResponse(
                status="error",
                message="Invalid model name."
            )

        retrievers = []

        try:
            vectorstore = load_vectorstore(model_provider)

            retrievers.append(
                vectorstore.as_retriever(
                    search_kwargs={"k": 3}
                )
            )

            logger.info("Uploaded PDF vectorstore loaded.")

        except Exception:

            logger.warning(
                "No uploaded PDF vectorstore found."
            )

        kb_vectorstore = Chroma(
            persist_directory=f"{KNOWLEDGE_BASE_VECTORSTORE}_{model_provider}",
            embedding_function=get_embeddings(model_provider)
        )

        retrievers.append(
            kb_vectorstore.as_retriever(
                search_kwargs={"k": 3}
            )
        )

        logger.info("Knowledge base vectorstore loaded.")

        combined_retriever = MergerRetriever(
            retrievers=retrievers
        )

        chain = build_llm_chain(
            model_provider,
            model_name,
            combined_retriever
        )

        if not chain:

            logger.error("Failed to build LLM chain.")

            return StandardAPIResponse(
                status="error",
                message="Failed to create LLM chain."
            )

        response = chain.invoke({
            "input": message
        })["answer"]

        logger.debug(
            "Chat response generated successfully"
        )

        return StandardAPIResponse(
            status="success",
            data=response
        )

    except Exception as e:

        logger.exception(
            "Chat endpoint encountered an error"
        )

        return StandardAPIResponse(
            status="error",
            message=str(e)
        )