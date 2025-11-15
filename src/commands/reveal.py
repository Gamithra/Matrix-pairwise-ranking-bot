"""Command: Reveal current rankings."""

import re
from typing import Optional

from storage import JSONStore
from config import Terminology


class RevealCommand:
    """Handle the 'reveal' command."""
    
    def __init__(self, store: JSONStore):
        self.store = store
    
    def parse_command(self, message: str, bot_name: str) -> bool:
        """
        Check if message is a reveal command.
        
        Expected formats:
        - @bot reveal
        - @bot reveal
        - @bot ranking
        - @bot rankings
        
        Args:
            message: The message text
            bot_name: The bot's name/localpart
            
        Returns:
            True if this is a reveal command
        """
        pattern = rf'@{re.escape(bot_name)}:?\s+(reveal|ranking|rankings)\s*$'
        return bool(re.search(pattern, message, re.IGNORECASE))
    
    def execute(self) -> str:
        """
        Generate the rankings display.
        
        Returns:
            Response message with rankings
        """
        term = Terminology.load()
        items = self.store.get_items_sorted_by_elo()
        
        if not items:
            return Terminology.get('messages.reveal_empty')
        
        # Build ranking message
        header = Terminology.get('messages.reveal_header')
        lines = [header, ""]
        
        for i, item in enumerate(items, 1):
            medal = ""
            if i == 1:
                medal = "🥇 "
            elif i == 2:
                medal = "🥈 "
            elif i == 3:
                medal = "🥉 "
            
            # Format: "1. 🥇 Item Name (Elo: 1623, Votes: 12)"
            elo_str = f"{item.elo:.0f}"
            votes_str = f"{item.votes_count} vote{'s' if item.votes_count != 1 else ''}"
            
            lines.append(f"{i}. {medal}**{item.name}** (elo: {elo_str}, {votes_str})")
        
        # Add footer
        total_votes = self.store.get_all_votes()
        lines.append("")
        lines.append(f"_total comparisons: {len(total_votes)}_")
        lines.append(f"_dm me to participate in ranking_")
        
        return "\n".join(lines)
