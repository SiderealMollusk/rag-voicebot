import streamlit as st
from typing import Tuple

def setup_page() -> None:
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="Voicebot - Chat with Documents",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def display_header() -> None:
    """Display the application header and description."""
    st.title("📄 Voicebot - Chat with Documents")
    st.subheader("Upload a document, ask questions, and get responses in both text and audio form.")
    st.write("This app allows you to interact with documents. It uses advanced NLP to process documents, "
             "allowing you to ask questions and get detailed answers in both text and audio format.")

def display_sidebar() -> None:
    """Display the sidebar with instructions."""
    st.sidebar.title("Instructions")
    st.sidebar.markdown("""
    **How to Use:**
     1. Upload a PDF or document file using the upload button below.
    2. Once processed, ask your question by typing or using voice input.
    3. Get responses in text and audio form.
    4. You can ask multiple questions sequentially, and your previous responses will remain visible.
    
    **Notes:**
    - The answers are based on the document you uploaded.
    - You can ask multiple questions one after another.
    - Your chat history will be visible throughout the session.
    """)

def create_columns() -> Tuple[object, object]:
    """Create and return two columns for the main layout.
    
    Returns:
        Tuple[object, object]: Left and right columns
    """
    return st.columns(2)

def initialize_session_state() -> None:
    """Initialize all session state variables."""
    if "data_stored" not in st.session_state:
        st.session_state["data_stored"] = False
    
    if "file_meta" not in st.session_state:
        st.session_state["file_meta"] = {}
    
    if "uploaded_file" not in st.session_state:
        st.session_state["uploaded_file"] = None
    
    if "pdf_processed" not in st.session_state:
        st.session_state["pdf_processed"] = False

def upload_section() -> object:
    """Create and return the file upload widget.
    
    Returns:
        object: Streamlit file uploader widget
    """
    return st.file_uploader("Upload your PDF file", type=["pdf"])

def process_button() -> bool:
    """Create and return the process button.
    
    Returns:
        bool: True if button is clicked, False otherwise
    """
    return st.button("Process")

def ask_another_question_button() -> bool:
    """Create and return the 'Ask Another Question' button.
    
    Returns:
        bool: True if button is clicked, False otherwise
    """
    return st.button("Ask Another Question")

def display_file_preview_header() -> None:
    """Display the file preview section header."""
    st.write("Uploaded File Preview")
