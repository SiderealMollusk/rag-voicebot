from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
import streamlit as st
from typing import List
from langchain.docstore.document import Document

from .config import (
    OPENAI_API_KEY,
    QDRANT_URL,
    QDRANT_API_KEY,
    COLLECTION_NAME,
    EMBEDDING_MODEL
)
from .logger import log_app, log_network

def send_to_qdrant(documents: List[Document], embedding_model: OpenAIEmbeddings) -> bool:
    """Send the document chunks to the Qdrant vector database.
    
    Args:
        documents: List of document chunks to store
        embedding_model: OpenAI embedding model instance
    
    Returns:
        bool: True if storage was successful, False otherwise
    """
    try:
        log_app(f"Preparing to store {len(documents)} documents in Qdrant collection: {COLLECTION_NAME}")
        log_network(f"Connecting to Qdrant at {QDRANT_URL}")
        
        log_app("Creating vector store from documents")
        Qdrant.from_documents(
            documents,
            embedding_model,
            url=QDRANT_URL,
            prefer_grpc=False,
            api_key=QDRANT_API_KEY,
            collection_name=COLLECTION_NAME,
            force_recreate=True
        )
        
        log_app("Successfully stored documents in Qdrant")
        return True
        
    except Exception as ex:
        error_msg = f"Failed to store data in the vector DB: {str(ex)}"
        log_app(error_msg, "error")
        st.error(error_msg)
        return False

def get_qdrant_store() -> Qdrant:
    """Initialize and return a Qdrant vector store instance.
    
    Returns:
        Qdrant: Initialized Qdrant vector store
    """
    try:
        # Initialize the embedding model
        log_network(f"Initializing OpenAI embeddings model: {EMBEDDING_MODEL}")
        embedding_model = OpenAIEmbeddings(
            openai_api_key=OPENAI_API_KEY,
            model=EMBEDDING_MODEL
        )
        log_app("Embedding model initialized successfully")

        # Initialize the Qdrant client
        log_network(f"Connecting to Qdrant server at {QDRANT_URL}")
        qdrant_client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY
        )
        log_app("Qdrant client connection established")

        # Create and return the Qdrant vector store
        log_app(f"Creating Qdrant vector store for collection: {COLLECTION_NAME}")
        vector_store = Qdrant(
            client=qdrant_client,
            collection_name=COLLECTION_NAME,
            embeddings=embedding_model
        )
        log_app("Vector store initialized successfully")
        
        return vector_store
        
    except Exception as ex:
        error_msg = f"Error initializing Qdrant store: {str(ex)}"
        log_app(error_msg, "error")
        raise Exception(error_msg)
