import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

class Config:
    """Central configuration management"""
    
    # Telegram API
    _api_id_str = os.getenv("API_ID", "0")
    API_ID = int(_api_id_str) if _api_id_str.isdigit() else 0
    API_HASH = os.getenv("API_HASH", "")
    
    # Session management
    SESSION_PASSWORD = os.getenv("SESSION_PASSWORD", "changeme")
    SESSIONS_DIR = Path(os.getenv("SESSIONS_DIR", "./sessions"))
    
    # Output and logging
    CSV_OUTPUT_DIR = Path(os.getenv("CSV_OUTPUT_DIR", "./output"))
    LOG_DIR = Path(os.getenv("LOG_DIR", "./logs"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Create directories if they don't exist
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    CSV_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    # Feature flags
    ENABLE_FLOODWAIT_HANDLING = True
    ENABLE_SESSION_ENCRYPTION = True
    
    # Delays (seconds)
    BROADCAST_DELAY_MIN = 30
    BROADCAST_DELAY_MAX = 60
    REQUEST_DELAY = 1
    
    # Scraping
    MEMBERS_BATCH_SIZE = 200
    MAX_MESSAGE_HISTORY = 100000
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is set"""
        if cls.API_ID == 0 or not cls.API_HASH:
            raise ValueError(
                "API_ID and API_HASH must be set in .env file. "
                "Get them from https://my.telegram.org/apps"
            )
