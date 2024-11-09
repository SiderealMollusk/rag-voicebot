import streamlit as st
from typing import Tuple
from .logger import log_app, log_user

def setup_page() -> None:
    """Configure the Streamlit page settings."""
    log_app("Initializing Streamlit page configuration")
    st.set_page_config(
        page_title="Voicebot - Chat with Documents",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    log_app("Page configuration complete")

def display_header() -> None:
    """Display the application header and description."""
    log_app("Rendering application header")
    st.title("📄 Voicebot - Chat with Documents")
    st.subheader("Upload a document, ask questions, and get responses in both text and audio form.")
    st.write("This app allows you to interact with documents. It uses advanced NLP to process documents, "
             "allowing you to ask questions and get detailed answers in both text and audio format.")
    log_app("Header display complete")

def display_sidebar() -> None:
    """Display the sidebar with instructions."""
    log_app("Rendering sidebar content")
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
    log_app("Sidebar display complete")

def create_columns() -> Tuple[object, object]:
    """Create and return two columns for the main layout.
    
    Returns:
        Tuple[object, object]: Left and right columns
    """
    log_app("Creating main layout columns")
    columns = st.columns(2)
    log_app("Layout columns created")
    return columns

def initialize_session_state() -> None:
    """Initialize all session state variables."""
    log_app("Initializing session state variables")
    
    if "data_stored" not in st.session_state:
        st.session_state["data_stored"] = False
        log_app("Initialized data_stored state: False")
    
    if "file_meta" not in st.session_state:
        st.session_state["file_meta"] = {}
        log_app("Initialized file_meta state: empty dict")
    
    if "uploaded_file" not in st.session_state:
        st.session_state["uploaded_file"] = None
        log_app("Initialized uploaded_file state: None")
    
    if "pdf_processed" not in st.session_state:
        st.session_state["pdf_processed"] = False
        log_app("Initialized pdf_processed state: False")
    
    log_app("Session state initialization complete")

def upload_section() -> object:
    """Create and return the file upload widget.
    
    Returns:
        object: Streamlit file uploader widget
    """
    log_app("Creating file upload widget")
    uploader = st.file_uploader("Upload your PDF file", type=["pdf"])
    if uploader is not None:
        log_user(f"File uploaded: {uploader.name}")
    return uploader

def process_button() -> bool:
    """Create and return the process button.
    
    Returns:
        bool: True if button is clicked, False otherwise
    """
    log_app("Creating process button")
    button_clicked = st.button("Process")
    if button_clicked:
        log_user("Process button clicked")
    return button_clicked

def ask_another_question_button() -> bool:
    """Create and return the 'Ask Another Question' button.
    
    Returns:
        bool: True if button is clicked, False otherwise
    """
    log_app("Creating 'Ask Another Question' button")
    button_clicked = st.button("Ask Another Question")
    if button_clicked:
        log_user("Ask Another Question button clicked")
    return button_clicked

def display_file_preview_header() -> None:
    """Display the file preview section header."""
    log_app("Displaying file preview header")
    st.write("Uploaded File Preview")
    log_app("File preview header displayed")

def update_session_state(key: str, value: any) -> None:
    """Update a session state variable and log the change.
    
    Args:
        key: The session state key to update
        value: The new value
    """
    try:
        old_value = st.session_state.get(key, None)
        st.session_state[key] = value
        log_app(f"Session state updated - {key}: {old_value} -> {value}")
    except Exception as e:
        log_app(f"Error updating session state {key}: {str(e)}", "error")
