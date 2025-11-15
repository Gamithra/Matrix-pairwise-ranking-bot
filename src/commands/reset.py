"""Command: Reset operations."""

import re
from typing import Optional

from storage import JSONStore


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
        Reset everything: delete all plandidates and votes.
        
        Returns:
            Response message
        """
        self.store.reset_all()
        return "🗑️ **reset complete** (all plandidates and votes have been cleared.)"
    
    def execute_rerank(self) -> str:
        """
        Reset rankings: clear all votes and reset Elo scores, but keep plandidates.
        
        Returns:
            Response message
        """
        plandidates = self.store.get_all_plandidates()
        
        if not plandidates:
            return "⚠️ no plandidates to rerank"
        
        self.store.reset_rankings()
        
        return f"🔄 **rankings reset** (all {len(plandidates)} plandidates have been reset to 1500 elo)"
