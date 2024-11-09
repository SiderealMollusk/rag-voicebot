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

def main():
    """Main application entry point."""
    # Set up the page
    setup_page()
    
    # Display header and sidebar
    display_header()
    display_sidebar()
    
    # Initialize session state
    initialize_session_state()
    initialize_chat_state()
    
    # Create two columns for layout
    col1, col2 = create_columns()
    
    with col1:
        # Left column: Upload and Chat
        st.header("Upload and Chat")
        
        # Step 1: Upload the PDF file
        uploaded_file = upload_section()
        if uploaded_file is not None:
            st.session_state["uploaded_file"] = uploaded_file
        
        # Step 2: Process the PDF when 'Process' button is clicked
        if (uploaded_file is not None or st.session_state["uploaded_file"] is not None) \
           and not st.session_state["pdf_processed"]:
            if process_button():
                success, file_meta = process_uploaded_file(
                    st.session_state["uploaded_file"]
                )
                if success:
                    st.session_state["data_stored"] = True
                    st.session_state["pdf_processed"] = True
                    st.session_state["file_meta"] = file_meta
                    st.success("Document successfully stored in the vector database.")
                else:
                    st.error("Failed to process the document.")
        
        # Step 3: Show the audio input if document is stored
        if st.session_state["data_stored"]:
            st.write("Ask Your Question")
            audio_input = process_audio_input(st.session_state["recording_key"])
            
            if audio_input:
                # Increment recording key for unique widget IDs
                st.session_state["recording_key"] += 1
                
                # Generate response from AI model
                bot_response = qa_ret(audio_input)
                
                # Add to chat history
                add_to_chat_history(
                    audio_input,
                    bot_response,
                    st.session_state["file_meta"]
                )
                
                # Display the chat history
                display_chat_history()
                
                # Place the record button under the latest answer
                if ask_another_question_button():
                    st.experimental_rerun()
    
    with col2:
        # Right column: Preview of the uploaded file
        display_file_preview_header()
        
        # Only display preview if there is chat history
        if len(st.session_state["chat_history"]) > 0:
            display_pdf_preview(st.session_state["uploaded_file"])

if __name__ == "__main__":
    main()
