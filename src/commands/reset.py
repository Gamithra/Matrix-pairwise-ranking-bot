"""Command: Reset operations."""

import re
from typing import Optional

from storage import JSONStore
from config import Terminology


class ResetCommand:
    """Handle reset commands."""
    
    def __init__(self, store: JSONStore):
        self.store = store
    
    def parse_reset_all_command(self, message: str, bot_name: str) -> bool:
        """
        Check if message is a reset all command.
        
        Expected formats:
        - @operator reset
        - @operator reset all
        - @operator clear all
        
        Args:
            message: The message text
            bot_name: The bot's name/localpart
            
        Returns:
            True if this is a reset all command
        """
        pattern = rf'@{re.escape(bot_name)}:?\s+(reset\s*(all)?|clear\s*all)\s*$'
        return bool(re.search(pattern, message, re.IGNORECASE))
    
    def parse_rerank_command(self, message: str, bot_name: str) -> bool:
        """
        Check if message is a rerank command.
        
        Expected formats:
        - @operator rerank
        - @operator reset rankings
        - @operator reset votes
        
        Args:
            message: The message text
            bot_name: The bot's name/localpart
            
        Returns:
            True if this is a rerank command
        """
        pattern = rf'@{re.escape(bot_name)}:?\s+(rerank|reset\s+(rankings?|votes?))\s*$'
        return bool(re.search(pattern, message, re.IGNORECASE))
    
    def execute_reset_all(self) -> str:
        """
        Reset everything: delete all items and votes.
        
        Returns:
            Response message
        """
        self.store.reset_all()
        return Terminology.get('messages.reset_all_confirm')
    
    def execute_rerank(self) -> str:
        """
        Reset rankings: clear all votes and reset Elo scores, but keep items.
        
        Returns:
            Response message
        """
        term = Terminology.load()
        items = self.store.get_all_items()
        
        if not items:
            item_plural = term.get('item_name_plural', 'items')
            return f"⚠️ No {item_plural} to rerank"
        
        self.store.reset_rankings()
        
        return Terminology.get('messages.rerank_confirm')
