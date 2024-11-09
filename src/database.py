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

def send_to_qdrant(documents: List[Document], embedding_model: OpenAIEmbeddings) -> bool:
    """Send the document chunks to the Qdrant vector database.
    
    Args:
        documents: List of document chunks to store
        embedding_model: OpenAI embedding model instance
    
    Returns:
        bool: True if storage was successful, False otherwise
    """
    try:
        Qdrant.from_documents(
            documents,
            embedding_model,
            url=QDRANT_URL,
            prefer_grpc=False,
            api_key=QDRANT_API_KEY,
            collection_name=COLLECTION_NAME,
            force_recreate=True
        )
        return True
    except Exception as ex:
        st.error(f"Failed to store data in the vector DB: {str(ex)}")
        return False

def get_qdrant_store() -> Qdrant:
    """Initialize and return a Qdrant vector store instance.
    
    Returns:
        Qdrant: Initialized Qdrant vector store
    """
    # Initialize the embedding model
    embedding_model = OpenAIEmbeddings(
        openai_api_key=OPENAI_API_KEY,
        model=EMBEDDING_MODEL
    )

    # Initialize the Qdrant client
    qdrant_client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY
    )

    # Create and return the Qdrant vector store
    return Qdrant(
        client=qdrant_client,
        collection_name=COLLECTION_NAME,
        embeddings=embedding_model
    )
