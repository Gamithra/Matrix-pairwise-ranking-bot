"""Configuration management for the Matrix ranking bot."""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Terminology:
    """Load and manage custom terminology for the bot."""
    
    _terminology = None
    
    @classmethod
    def load(cls):
        """Load terminology from JSON file."""
        if cls._terminology is not None:
            return cls._terminology
        
        # Try to load terminology.json from project root
        terminology_path = Path("terminology.json")
        if not terminology_path.exists():
            # Fall back to example/default
            terminology_path = Path("terminology.example.json")
        
        if terminology_path.exists():
            with open(terminology_path, 'r') as f:
                cls._terminology = json.load(f)
        else:
            # Absolute fallback if no files exist
            cls._terminology = {
                "item_name": "item",
                "item_name_plural": "items",
                "item_name_capitalized": "Item",
                "messages": {
                    "add_success": "Added '{item}' to the ranking list.",
                    "add_duplicate": "'{item}' is already in the list.",
                    "reveal_header": "📊 **Current rankings** 📊",
                    "reveal_empty": "No items to rank yet. Add some with `@{bot_name} add <item>`",
                    "reset_all_confirm": "Reset complete. All items, votes, and rankings have been cleared.",
                    "rerank_confirm": "Rankings reset. All votes cleared, but items remain in the system.",
                    "vote_intro": "Let's rank these items. Which one do you prefer?",
                    "vote_option_format": "**{number}.** {item}",
                    "vote_progress": "Progress: {done}/{total} comparisons completed",
                    "vote_complete": "All comparisons complete! Rankings are now up to date.",
                    "vote_invalid": "Please enter 1 or 2 to make your selection.",
                    "help_text": "Available commands:\n\n**In rooms:**\n- `@{bot_name} add <item>` - Add a new item to rank\n- `@{bot_name} reveal` - Display current rankings\n- `@{bot_name} reset all` - Clear all data (items, votes, rankings)\n- `@{bot_name} rerank` - Reset votes and rankings (keeps items)\n\n**In direct messages:**\n- Message me to start pairwise ranking comparisons\n\nRankings are calculated using the Elo rating algorithm."
                }
            }
        
        return cls._terminology
    
    @classmethod
    def get(cls, key: str, **kwargs) -> str:
        """Get a terminology value with optional formatting."""
        term = cls.load()
        
        # Navigate nested keys (e.g., "messages.add_success")
        value = term
        for k in key.split('.'):
            value = value.get(k, key)
        
        # Format if kwargs provided
        if isinstance(value, str) and kwargs:
            # Add common substitutions
            kwargs.setdefault('bot_name', term.get('bot_name', 'RankBot'))
            return value.format(**kwargs)
        
        return value


class Config:
    """Bot configuration."""
    
    # Matrix settings
    HOMESERVER = os.getenv("MATRIX_HOMESERVER", "https://matrix.org")
    USER_ID = os.getenv("MATRIX_USER_ID")
    PASSWORD = os.getenv("MATRIX_PASSWORD")
    ACCESS_TOKEN = os.getenv("MATRIX_ACCESS_TOKEN")  # Alternative to password
    
    # Bot settings
    DISPLAY_NAME = os.getenv("BOT_DISPLAY_NAME", "RankBot")
    
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
        return "rankbot"
    
    @classmethod
    def is_user_allowed(cls, user_id: str) -> bool:
        """Check if a user is allowed to use the bot."""
        if not cls.ALLOWED_USERS:
            # If no whitelist is set, allow everyone
            return True
        
        allowed_list = [u.strip() for u in cls.ALLOWED_USERS.split(',') if u.strip()]
        return user_id in allowed_list
