import streamlit as st
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
from typing import Optional

from .config import DEFAULT_LANGUAGE, TTS_TLD

def process_audio_input(recording_key: int) -> Optional[str]:
    """Capture audio from mic and convert it to text using speech-to-text.
    
    Args:
        recording_key: Unique identifier for the recording session
    
    Returns:
        str: Transcribed text from the audio input, or None if no input
    """
    unique_key = f"STT-{recording_key}"
    
    # Capture audio input from the mic and convert it to text
    transcribed_text = speech_to_text(
        language=DEFAULT_LANGUAGE,
        use_container_width=True,
        just_once=True,
        key=unique_key
    )
    
    return transcribed_text

def text_to_speech(text: str, lang: str = DEFAULT_LANGUAGE) -> BytesIO:
    """Convert text to speech using gTTS.
    
    Args:
        text: Text to convert to speech
        lang: Language code for text-to-speech conversion
    
    Returns:
        BytesIO: Audio data buffer containing the speech
    """
    # Initialize gTTS with the given text and language
    tts = gTTS(text=text, lang=lang, tld=TTS_TLD)
    
    # Create an in-memory buffer for audio data
    audio_data = BytesIO()
    
    # Write the generated audio to the buffer
    tts.write_to_fp(audio_data)
    
    # Reset buffer to the start
    audio_data.seek(0)
    
    return audio_data
