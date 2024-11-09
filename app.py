from src.main import main
from src.logger import log_app

if __name__ == "__main__":
    try:
        log_app("Starting Voicebot application from app.py")
        main()
        log_app("Application terminated normally")
    except Exception as e:
        log_app(f"Fatal error during application startup: {str(e)}", "error")
        raise
