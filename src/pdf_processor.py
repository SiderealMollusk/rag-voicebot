import streamlit as st
import tempfile
import base64
from typing import Tuple, Optional, Dict
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings

from .config import (
    OPENAI_API_KEY,
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)
from .database import send_to_qdrant
from .logger import log_app, log_network

def process_uploaded_file(uploaded_file) -> Tuple[bool, Dict]:
    """Process the uploaded PDF file and store its content in vector DB.
    
    Args:
        uploaded_file: StreamlitUploadedFile object containing the PDF
    
    Returns:
        Tuple[bool, Dict]: Success status and file metadata
    """
    if uploaded_file is None:
        log_app("No file uploaded", "warning")
        return False, {}

    # Create file metadata
    file_meta = {
        "file_name": uploaded_file.name,
        "file_size": uploaded_file.size / 1024  # Size in KB
    }
    log_app(f"Processing uploaded file: {file_meta['file_name']} ({file_meta['file_size']:.2f} KB)")

    try:
        # Save uploaded file to temporary location
        log_app("Saving file to temporary location")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name
            log_app(f"Temporary file created at: {temp_file_path}")

        # Load and extract text from the PDF
        log_app("Loading PDF and extracting text")
        loader = PyPDFLoader(temp_file_path)
        pages = loader.load()
        document_text = "".join([page.page_content for page in pages])
        log_app(f"Extracted {len(pages)} pages, total text length: {len(document_text)} chars")

        # Split the document into chunks
        log_app(f"Splitting text into chunks (size: {CHUNK_SIZE}, overlap: {CHUNK_OVERLAP})")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        chunks = text_splitter.create_documents([document_text])
        log_app(f"Created {len(chunks)} text chunks")

        # Create the embedding model
        log_network(f"Initializing OpenAI embeddings model: {EMBEDDING_MODEL}")
        embedding_model = OpenAIEmbeddings(
            openai_api_key=OPENAI_API_KEY,
            model=EMBEDDING_MODEL
        )

        # Store in vector database
        log_app("Sending chunks to Qdrant vector store")
        if send_to_qdrant(chunks, embedding_model):
            log_app("Successfully stored document in vector database")
            return True, file_meta
        
        log_app("Failed to store document in vector database", "error")
        return False, file_meta

    except Exception as ex:
        error_msg = f"Error processing PDF: {str(ex)}"
        log_app(error_msg, "error")
        st.error(error_msg)
        return False, file_meta

def display_pdf_preview(uploaded_file: Optional[object]) -> None:
    """Display a preview of the uploaded PDF file.
    
    Args:
        uploaded_file: StreamlitUploadedFile object containing the PDF
    """
    if uploaded_file:
        try:
            log_app(f"Generating preview for PDF: {uploaded_file.name}")
            
            # Process and display PDF
            log_app("Creating temporary file for preview")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name
                log_app(f"Preview temp file created at: {temp_file_path}")

            # Read the file as base64
            log_app("Converting PDF to base64 for display")
            with open(temp_file_path, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')

            # Embed PDF preview using iframe
            log_app("Embedding PDF preview in iframe")
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
            log_app("PDF preview displayed successfully")
            
        except Exception as ex:
            error_msg = f"Error displaying PDF preview: {str(ex)}"
            log_app(error_msg, "error")
            st.error(error_msg)
