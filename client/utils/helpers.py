from utils.api import (
  chat,
  get_supported_llm,
  get_supported_models,
  upload_and_process_pdfs,
)


def get_model_providers() -> list[str]:
  return get_supported_llm()

def get_models(model_provider) -> list[str]:
  if not model_provider:
    return []
  return get_supported_models(model_provider)

def process_uploaded_pdfs(model_provider, uploaded_files) -> str:
  return upload_and_process_pdfs(model_provider, uploaded_files)

def process_user_input(model_provider, model_name, user_input) -> str:
  return chat(model_provider, model_name, user_input)

