import streamlit as st

from datetime import datetime

from utils.helpers import process_user_input


def render_user_input(model_provider, model):

    disable_input = (
        st.session_state.get("unsubmitted_files", False)
        or not model_provider
        or not model
    )

    question = st.chat_input(
        "💬 Ask something...",
        disabled=disable_input
    )

    if not question:
        return

    with st.chat_message("user"):
        st.write(question)

    with st.spinner("Thinking..."):

        try:
            output = process_user_input(
                model_provider,
                model,
                question
            )

            with st.chat_message("assistant"):
                st.write(output)

            pdf_names = [
                f.name
                for f in st.session_state.get("pdf_files", [])
            ]

            st.session_state.chat_history.append(
                (
                    question,
                    output,
                    model_provider,
                    model,
                    pdf_names,
                    datetime.now()
                )
            )

        except Exception as e:
            st.error(f"Error: {str(e)}")


def render_uploaded_files_expander():

    uploaded_files = st.session_state.get(
        f"uploaded_files_{st.session_state.uploader_key}",
        []
    )

    if uploaded_files and not st.session_state.get("unsubmitted_files"):

        with st.expander(
            "📂 Active Uploaded PDFs",
            expanded=False
        ):

            st.markdown(f"""
            <div style="
                padding:10px;
                border-radius:10px;
                background:#1E1E1E;
                margin-bottom:12px;
            ">
                📚 <b>{len(uploaded_files)}</b> PDF(s) active
            </div>
            """, unsafe_allow_html=True)

            for f in uploaded_files:

                st.markdown(f"""
                <div style="
                    padding:8px;
                    border-radius:8px;
                    background:#262730;
                    margin-bottom:8px;
                ">
                    📄 {f.name}
                </div>
                """, unsafe_allow_html=True)


def render_chat_history():

    for q, a, *_ in st.session_state.get("chat_history", []):

        with st.chat_message("user"):
            st.write(q)

        with st.chat_message("assistant"):
            st.write(a)