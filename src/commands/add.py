"""Command: Add a new item to rank."""

import re
from typing import Optional

from storage import JSONStore
from config import Terminology


class AddCommand:
    """Handle the 'add' command."""
    
    def __init__(self, store: JSONStore):
        self.store = store
    
    def parse_command(self, message: str, bot_name: str) -> Optional[str]:
        """
        Parse an add command from a message.
        
        Expected formats:
        - @botname add Some item name
        - @botname: add Some item name
        
        Args:
            message: The message text
            bot_name: The bot's name/localpart
            
        Returns:
            The item name to add, or None if not a valid add command
        """
        # Pattern: @botname add <item>
        # Allow optional colon after mention
        pattern = rf'@{re.escape(bot_name)}:?\s+add\s+(.+)'
        match = re.search(pattern, message, re.IGNORECASE)
        
        if match:
            item_name = match.group(1).strip()
            return item_name if item_name else None
        
        return None
    
    def execute(self, item_name: str, user_id: str) -> str:
        """
        Add an item to rank.
        
        Args:
            item_name: Name of the item to add
            user_id: User ID who is adding it
            
        Returns:
            Response message
        """
        term = Terminology.load()
        item_singular = term.get('item_name', 'item')
        
        if not item_name:
            return f"Please provide a {item_singular} name."
        
        item = self.store.add_plandidate(item_name, user_id)
        
        # Check if it was already added
        existing = self.store.get_all_plandidates()
        is_duplicate = len([p for p in existing if p.name.lower() == item_name.lower()]) > 1
        
        if is_duplicate:
            return Terminology.get('messages.add_duplicate', item=item.name)
        
        return Terminology.get('messages.add_success', item=item.name)
