"""Command: Add a new plandidate."""

import re
from typing import Optional

from storage import JSONStore


class AddCommand:
    """Handle the 'add' command."""
    
    def __init__(self, store: JSONStore):
        self.store = store
    
    def parse_command(self, message: str, bot_name: str) -> Optional[str]:
        """
        Parse an add command from a message.
        
        Expected formats:
        - @planter add Some plandidate name
        - @planter: add Some plandidate name
        
        Args:
            message: The message text
            bot_name: The bot's name/localpart
            
        Returns:
            The plandidate name to add, or None if not a valid add command
        """
        # Pattern: @botname add <plandidate>
        # Allow optional colon after mention
        pattern = rf'@{re.escape(bot_name)}:?\s+add\s+(.+)'
        match = re.search(pattern, message, re.IGNORECASE)
        
        if match:
            plandidate_name = match.group(1).strip()
            return plandidate_name if plandidate_name else None
        
        return None
    
    def execute(self, plandidate_name: str, user_id: str) -> str:
        """
        Add a plandidate.
        
        Args:
            plandidate_name: Name of the plandidate to add
            user_id: User ID who is adding it
            
        Returns:
            Response message
        """
        if not plandidate_name:
            return "❌ bro please provide a plandidate name"
        
        plandidate = self.store.add_plandidate(plandidate_name, user_id)
        
        # Check if it was already added (same object returned)
        existing = self.store.get_all_plandidates()
        if len([p for p in existing if p.name.lower() == plandidate_name.lower()]) > 0:
            return f"✅ bro added plandidate: **{plandidate.name}**"
        
        return f"✅ bro added plandidate: **{plandidate.name}**"
