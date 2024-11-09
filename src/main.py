import streamlit as st

from .ui import (
    setup_page,
    display_header,
    display_sidebar,
    create_columns,
    initialize_session_state,
    upload_section,
    process_button,
    ask_another_question_button,
    display_file_preview_header
)
from .chat import (
    initialize_chat_state,
    qa_ret,
    add_to_chat_history,
    display_chat_history
)
from .pdf_processor import (
    process_uploaded_file,
    display_pdf_preview
)
from .audio import process_audio_input
from .logger import log_app, log_user

def main():
    """Main application entry point."""
    try:
        log_app("Starting Voicebot application")
        
        # Set up the page
        log_app("Setting up Streamlit page")
        setup_page()
        
        # Display header and sidebar
        log_app("Rendering main UI components")
        display_header()
        display_sidebar()
        
        # Initialize session state
        log_app("Initializing application state")
        initialize_session_state()
        initialize_chat_state()
        
        # Create two columns for layout
        log_app("Creating main layout")
        col1, col2 = create_columns()
        
        with col1:
            # Left column: Upload and Chat
            log_app("Rendering left column: Upload and Chat section")
            st.header("Upload and Chat")
            
            # Step 1: Upload the PDF file
            log_app("Handling file upload section")
            uploaded_file = upload_section()
            if uploaded_file is not None:
                log_app(f"New file uploaded: {uploaded_file.name}")
                st.session_state["uploaded_file"] = uploaded_file
            
            # Step 2: Process the PDF when 'Process' button is clicked
            if (uploaded_file is not None or st.session_state["uploaded_file"] is not None) \
               and not st.session_state["pdf_processed"]:
                if process_button():
                    log_app("Processing uploaded PDF file")
                    success, file_meta = process_uploaded_file(
                        st.session_state["uploaded_file"]
                    )
                    if success:
                        log_app("PDF processing successful")
                        st.session_state["data_stored"] = True
                        st.session_state["pdf_processed"] = True
                        st.session_state["file_meta"] = file_meta
                        st.success("Document successfully stored in the vector database.")
                    else:
                        log_app("PDF processing failed", "error")
                        st.error("Failed to process the document.")
            
            # Step 3: Show the audio input if document is stored
            if st.session_state["data_stored"]:
                log_app("Initializing audio input section")
                st.write("Ask Your Question")
                audio_input = process_audio_input(st.session_state["recording_key"])
                
                if audio_input:
                    log_user(f"Received audio input: {audio_input}")
                    
                    # Increment recording key for unique widget IDs
                    st.session_state["recording_key"] += 1
                    log_app(f"Incremented recording key to {st.session_state['recording_key']}")
                    
                    # Generate response from AI model
                    log_app("Generating AI response")
                    bot_response = qa_ret(audio_input)
                    
                    # Add to chat history
                    log_app("Updating chat history")
                    add_to_chat_history(
                        audio_input,
                        bot_response,
                        st.session_state["file_meta"]
                    )
                    
                    # Display the chat history
                    log_app("Displaying updated chat history")
                    display_chat_history()
                    
                    # Place the record button under the latest answer
                    if ask_another_question_button():
                        log_app("Rerunning app for new question")
                        st.experimental_rerun()
        
        with col2:
            # Right column: Preview of the uploaded file
            log_app("Rendering right column: File preview section")
            display_file_preview_header()
            
            # Only display preview if there is chat history
            if len(st.session_state["chat_history"]) > 0:
                log_app("Displaying PDF preview")
                display_pdf_preview(st.session_state["uploaded_file"])
        
        log_app("Application rendering complete")

    except Exception as e:
        error_msg = f"Critical application error: {str(e)}"
        log_app(error_msg, "error")
        st.error(error_msg)

if __name__ == "__main__":
    main()
