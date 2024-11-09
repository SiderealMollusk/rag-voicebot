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

def process_uploaded_file(uploaded_file) -> Tuple[bool, Dict]:
    """Process the uploaded PDF file and store its content in vector DB.
    
    Args:
        uploaded_file: StreamlitUploadedFile object containing the PDF
    
    Returns:
        Tuple[bool, Dict]: Success status and file metadata
    """
    if uploaded_file is None:
        return False, {}

    # Create file metadata
    file_meta = {
        "file_name": uploaded_file.name,
        "file_size": uploaded_file.size / 1024  # Size in KB
    }

    try:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        # Load and extract text from the PDF
        loader = PyPDFLoader(temp_file_path)
        pages = loader.load()
        document_text = "".join([page.page_content for page in pages])

        # Split the document into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        chunks = text_splitter.create_documents([document_text])

        # Create the embedding model
        embedding_model = OpenAIEmbeddings(
            openai_api_key=OPENAI_API_KEY,
            model=EMBEDDING_MODEL
        )

        # Store in vector database
        if send_to_qdrant(chunks, embedding_model):
            return True, file_meta
        
        return False, file_meta

    except Exception as ex:
        st.error(f"Error processing PDF: {str(ex)}")
        return False, file_meta

def display_pdf_preview(uploaded_file: Optional[object]) -> None:
    """Display a preview of the uploaded PDF file.
    
    Args:
        uploaded_file: StreamlitUploadedFile object containing the PDF
    """
    if uploaded_file:
        try:
            # Process and display PDF
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name

            # Read the file as base64
            with open(temp_file_path, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')

            # Embed PDF preview using iframe
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
            
        except Exception as ex:
            st.error(f"Error displaying PDF preview: {str(ex)}")
