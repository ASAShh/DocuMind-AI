import streamlit as st

from state.session import setup_session_state, is_chat_ready
from components.chat import (
  render_chat_history,
  render_uploaded_files_expander,
  render_user_input
)
from components.sidebar import (
  render_model_selector,
  sidebar_file_upload,
  sidebar_provider_change_check,
  sidebar_utilities
)


def main():
  st.set_page_config(page_title="RAG PDFBot", layout="centered")
  st.markdown("""
  <style>

  section[data-testid="stSidebar"] {
      background-color: #111111;
  }

  section[data-testid="stSidebar"] * {
      color: white;
  }

  .stButton button {
      border-radius: 10px;
      height: 45px;
      font-weight: bold;
  }

  </style>
  """, unsafe_allow_html=True)

  st.title("🧠 DocuMind AI")
  st.caption("Chat with PDFs + Knowledge Base")

  setup_session_state()

  with st.sidebar:
    with st.expander("⚙️AI Settings", expanded=True):
      model_provider, model = render_model_selector()

      sidebar_file_upload(model_provider)

      sidebar_provider_change_check(model_provider, model)

    sidebar_utilities()

  if st.session_state.get("unsubmitted_files", False):
    st.warning("📄 New PDFs uploaded. Please submit before chatting.")

  if st.session_state.get("pdf_files", []):
    render_uploaded_files_expander()

  if st.session_state.get("chat_history", []):
    render_chat_history()

  render_user_input(model_provider, model)


if __name__ == "__main__":
    main()