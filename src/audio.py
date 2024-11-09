import streamlit as st
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
from typing import Optional

from .config import DEFAULT_LANGUAGE, TTS_TLD
from .logger import log_app, log_user, log_network

def process_audio_input(recording_key: int) -> Optional[str]:
    """Capture audio from mic and convert it to text using speech-to-text.
    
    Args:
        recording_key: Unique identifier for the recording session
    
    Returns:
        str: Transcribed text from the audio input, or None if no input
    """
    try:
        unique_key = f"STT-{recording_key}"
        log_app(f"Starting speech-to-text session with key: {unique_key}")
        
        # Capture audio input from the mic and convert it to text
        log_app("Listening for user audio input...")
        transcribed_text = speech_to_text(
            language=DEFAULT_LANGUAGE,
            use_container_width=True,
            just_once=True,
            key=unique_key
        )
        
        if transcribed_text:
            log_user(f"Speech transcribed: {transcribed_text}")
            return transcribed_text
        else:
            log_app("No speech detected or transcription failed")
            return None
            
    except Exception as e:
        log_app(f"Error in speech-to-text processing: {str(e)}", "error")
        return None

def text_to_speech(text: str, lang: str = DEFAULT_LANGUAGE) -> BytesIO:
    """Convert text to speech using gTTS.
    
    Args:
        text: Text to convert to speech
        lang: Language code for text-to-speech conversion
    
    Returns:
        BytesIO: Audio data buffer containing the speech
    """
    try:
        log_app(f"Starting text-to-speech conversion for text length: {len(text)} chars")
        log_app(f"Using language: {lang}, TLD: {TTS_TLD}")
        
        # Initialize gTTS with the given text and language
        log_network("Initializing gTTS service")
        tts = gTTS(text=text, lang=lang, tld=TTS_TLD)
        
        # Create an in-memory buffer for audio data
        audio_data = BytesIO()
        
        # Write the generated audio to the buffer
        log_network("Generating audio from text")
        tts.write_to_fp(audio_data)
        
        # Reset buffer to the start
        audio_data.seek(0)
        
        log_app("Text-to-speech conversion completed successfully")
        return audio_data
        
    except Exception as e:
        error_msg = f"Error in text-to-speech conversion: {str(e)}"
        log_app(error_msg, "error")
        raise Exception(error_msg)
