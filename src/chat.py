import streamlit as st
from typing import Dict, Any
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import ChatOpenAI

from .config import OPENAI_API_KEY, CHAT_MODEL, TEMPERATURE
from .database import get_qdrant_store
from .audio import text_to_speech
from .logger import log_app, log_user, log_bot, log_network

def qa_ret(input_query: str) -> str:
    """Generate a response using RAG (Retrieval Augmented Generation).
    
    Args:
        input_query: User's question
    
    Returns:
        str: Generated response from the AI model
    """
    try:
        log_app(f"Starting RAG chain for query")
        log_user(f"Query: {input_query}")
        
        # Get Qdrant store
        log_app("Initializing Qdrant store")
        qdrant_store = get_qdrant_store()
        
        # Define the template for generating responses
        template = """
        You are a helpful and dedicated female assistant. Your primary role is to assist the user by providing accurate
        and thoughtful answers based on the given context. If the user asks any questions related to the provided
        information, respond in a courteous and professional manner.
        {context}
        **Question:** {question}
        """
        
        # Create chat prompt template
        prompt = ChatPromptTemplate.from_template(template)
        log_app("Created chat prompt template")

        # Configure retriever
        log_app("Configuring retriever with k=4")
        retriever = qdrant_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )

        # Set up parallel execution
        log_app("Setting up parallel execution chain")
        setup_and_retrieval = RunnableParallel(
            {"context": retriever, "question": RunnablePassthrough()}
        )

        # Initialize the GPT model
        log_network(f"Initializing ChatGPT model: {CHAT_MODEL}")
        model = ChatOpenAI(
            model_name=CHAT_MODEL,
            temperature=TEMPERATURE,
            openai_api_key=OPENAI_API_KEY
        )

        # Chain the components
        output_parser = StrOutputParser()
        rag_chain = setup_and_retrieval | prompt | model | output_parser
        log_app("RAG chain assembled")

        # Generate response
        log_network("Sending request to OpenAI")
        response = rag_chain.invoke(input_query)
        log_bot(f"Generated response: {response[:100]}...")  # Log first 100 chars
        return response

    except Exception as ex:
        error_msg = f"Error in qa_ret: {str(ex)}"
        log_app(error_msg, "error")
        return f"Error: {str(ex)}"

def add_to_chat_history(user_input: str, bot_response: str, file_meta: Dict[str, Any]) -> None:
    """Add a new interaction to the chat history.
    
    Args:
        user_input: User's question or input
        bot_response: Assistant's response
        file_meta: Metadata about the file being discussed
    """
    log_app("Adding new interaction to chat history")
    
    # Convert bot's response to audio
    log_app("Converting response to audio")
    audio_response = text_to_speech(bot_response)
    
    # Add to chat history
    st.session_state["chat_history"].append({
        "user_input": user_input,
        "bot_response": bot_response,
        "bot_audio": audio_response,
        "file_meta": file_meta
    })
    log_app("Chat history updated successfully")

def display_chat_history() -> None:
    """Display the chat history with user inputs and assistant responses."""
    log_app(f"Displaying chat history with {len(st.session_state['chat_history'])} messages")
    
    for chat in st.session_state["chat_history"]:
        # Display user input
        with st.chat_message("user"):
            st.write(f"**You:** {chat['user_input']}")
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.write(f"**Bot:** {chat['bot_response']}")
            st.audio(chat["bot_audio"], format="audio/mp3")
        
        # Add divider
        st.write("---")

def initialize_chat_state() -> None:
    """Initialize chat-related session state variables."""
    log_app("Initializing chat state")
    
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
        log_app("Created new chat history")
    
    if "recording_key" not in st.session_state:
        st.session_state["recording_key"] = 0
        log_app("Initialized recording key")
