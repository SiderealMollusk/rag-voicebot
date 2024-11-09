import logging
from datetime import datetime
from typing import Optional

# ANSI color codes
COLORS = {
    'YELLOW': '\033[93m',  # App/System
    'BLUE': '\033[94m',    # Network
    'GREEN': '\033[92m',   # User
    'MAGENTA': '\033[95m', # Bot
    'RESET': '\033[0m'     # Reset color
}

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        # Save original levelname
        orig_levelname = record.levelname
        
        # Add color based on logger name
        if hasattr(record, 'color'):
            record.levelname = f"{record.color}{record.levelname}{COLORS['RESET']}"
        
        # Format the message
        result = super().format(record)
        
        # Restore original levelname
        record.levelname = orig_levelname
        return result

class ColoredLogger:
    @staticmethod
    def setup_logger(name: str, color: str, level: int = logging.INFO) -> logging.Logger:
        """
        Set up a colored logger for a specific component
        
        Args:
            name: Name of the logger
            color: Color code from COLORS dict
            level: Logging level
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # Create handler if none exists
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(level)
            
            # Create formatter
            formatter = ColoredFormatter(
                fmt='%(asctime)s [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        # Add color as a filter
        def add_color(record):
            record.color = color
            return True
        
        logger.addFilter(add_color)
        return logger

# Create loggers for different components
app_logger = ColoredLogger.setup_logger('app', COLORS['YELLOW'])
network_logger = ColoredLogger.setup_logger('network', COLORS['BLUE'])
user_logger = ColoredLogger.setup_logger('user', COLORS['GREEN'])
bot_logger = ColoredLogger.setup_logger('bot', COLORS['MAGENTA'])

# Convenience functions
def log_app(msg: str, level: str = 'info'):
    getattr(app_logger, level.lower())(msg)

def log_network(msg: str, level: str = 'info'):
    getattr(network_logger, level.lower())(msg)

def log_user(msg: str, level: str = 'info'):
    getattr(user_logger, level.lower())(msg)

def log_bot(msg: str, level: str = 'info'):
    getattr(bot_logger, level.lower())(msg)

# Example usage:
if __name__ == "__main__":
    log_app("Application started")
    log_network("API request initiated")
    log_user("User input received")
    log_bot("Bot response generated")
