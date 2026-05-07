import streamlit as st


def setup_session_state():
  default_state = {
    "chat_history": [],
    "chat_ready": True,
    "pdf_files": [],
    "last_provider": None,
    "unsubmitted_files": False,
    "uploader_key": 0
  }

  for key, default in default_state.items():
    if key not in st.session_state:
      st.session_state[key] = default

def is_chat_ready():
  return (
     not st.session_state.get("unsubmitted_files")
  )
