"""Configuration management for the Planter bot."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Bot configuration."""
    
    # Matrix settings
    HOMESERVER = os.getenv("MATRIX_HOMESERVER", "https://matrix.org")
    USER_ID = os.getenv("MATRIX_USER_ID")
    PASSWORD = os.getenv("MATRIX_PASSWORD")
    ACCESS_TOKEN = os.getenv("MATRIX_ACCESS_TOKEN")  # Alternative to password
    
    # Bot settings
    DISPLAY_NAME = os.getenv("BOT_DISPLAY_NAME", "Planter Bot")
    
    # Security: Allowed users (comma-separated list of Matrix user IDs)
    # Leave empty to allow everyone
    ALLOWED_USERS = os.getenv("ALLOWED_USERS", "").strip()
    
    # Data directory
    DATA_DIR = os.getenv("DATA_DIR", "./data")
    
    # Store directory for matrix-nio (for encryption keys, sync tokens, etc.)
    STORE_DIR = os.path.join(DATA_DIR, "store")
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.USER_ID:
            raise ValueError("MATRIX_USER_ID environment variable is required")
        if not cls.PASSWORD and not cls.ACCESS_TOKEN:
            raise ValueError("Either MATRIX_PASSWORD or MATRIX_ACCESS_TOKEN environment variable is required")
        
        # Create directories
        Path(cls.DATA_DIR).mkdir(exist_ok=True)
        Path(cls.STORE_DIR).mkdir(exist_ok=True)
    
    @classmethod
    def get_bot_mention_pattern(cls) -> str:
        """Get a pattern to match bot mentions."""
        # Extract the localpart from the user ID (@localpart:homeserver)
        if cls.USER_ID:
            localpart = cls.USER_ID.split(':')[0].lstrip('@')
            return localpart
        return "planter"
    
    @classmethod
    def is_user_allowed(cls, user_id: str) -> bool:
        """Check if a user is allowed to use the bot."""
        if not cls.ALLOWED_USERS:
            # If no whitelist is set, allow everyone
            return True
        
        allowed_list = [u.strip() for u in cls.ALLOWED_USERS.split(',') if u.strip()]
        return user_id in allowed_list
