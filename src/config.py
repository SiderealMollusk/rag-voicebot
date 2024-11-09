import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API keys and URLs configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Collection configuration
COLLECTION_NAME = "xeven_voicebot"

# Model configuration
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"
TEMPERATURE = 0.3

# Text splitting configuration
CHUNK_SIZE = 300
CHUNK_OVERLAP = 40

# Language configuration
DEFAULT_LANGUAGE = 'en'
TTS_TLD = 'com.au'  # Top Level Domain for text-to-speech accent
