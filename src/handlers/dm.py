"""Handler for DM voting interactions."""

from typing import Optional

from nio import AsyncClient, RoomMessageText

from storage import JSONStore, UserVotingSession
from ranking import EloRanking, PairSelector


class DMHandler:
    """Handle direct message voting interactions."""
    
    def __init__(self, client: AsyncClient, store: JSONStore, elo: EloRanking):
        self.client = client
        self.store = store
        self.elo = elo
    
    async def handle_dm(self, room_id: str, user_id: str, message: str):
        """
        Handle a message in a DM room.
        
        Args:
            room_id: The room ID
            user_id: The user who sent the message
            message: The message content
        """
        message = message.strip()
        
        # Get or create session
        session = self.store.get_session(user_id)
        
        # Check if user is responding to a voting prompt
        if session and session.current_pair:
            await self._handle_vote_response(room_id, user_id, message, session)
        else:
            # Start a new voting session
            await self._start_voting(room_id, user_id)
    
    async def _start_voting(self, room_id: str, user_id: str):
        """Start or continue a voting session for a user."""
        plandidates = self.store.get_all_plandidates()
        
        if len(plandidates) < 2:
            await self._send_message(
                room_id,
                "there aren't enough plandidates to compare yet! "
                "we need at least 2. "
                "tag me with `add <plandidate>` to add some"
            )
            return
        
        # Get pairs the user has already voted on
        voted_pairs = self.store.get_user_voted_pairs(user_id)
        
        # Get the next pair
        next_pair = PairSelector.get_next_pair(plandidates, voted_pairs)
        
        if not next_pair:
            # User has voted on all pairs!
            await self._send_message(
                room_id,
                "🎉 You've voted on all possible pairs! Thank you for your contribution.\n\n"
                "Check the rankings in a room by tagging me with `reveal`"
            )
            return
        
        # Save session
        session = UserVotingSession(user_id=user_id, current_pair=(next_pair[0].id, next_pair[1].id))
        self.store.save_session(session)
        
        # Send voting prompt
        remaining = PairSelector.count_remaining_pairs(len(plandidates), len(voted_pairs))
        
        await self._send_message(
            room_id,
            f"Which plandidate do you prefer?\n\n"
            f"**1.** {next_pair[0].name}\n"
            f"**2.** {next_pair[1].name}\n\n"
            f"Reply with **1** or **2**\n\n"
            f"_({remaining} pair{'s' if remaining != 1 else ''} remaining)_"
        )
    
    async def _handle_vote_response(self, room_id: str, user_id: str, 
                                   message: str, session: UserVotingSession):
        """
        Handle a user's vote response.
        
        Args:
            room_id: The room ID
            user_id: The user ID
            message: The message content (should be "1" or "2")
            session: The user's current voting session
        """
        # Parse the choice
        choice = message.strip()
        
        if choice not in ["1", "2"]:
            await self._send_message(
                room_id,
                "Please reply with **1** or **2** to choose your preference."
            )
            return
        
        # Get the plandidates from the session
        plandidate_a = self.store.get_plandidate_by_id(session.current_pair[0])
        plandidate_b = self.store.get_plandidate_by_id(session.current_pair[1])
        
        if not plandidate_a or not plandidate_b:
            await self._send_message(room_id, "❌ Error: Plandidate not found. Starting over...")
            self.store.clear_session(user_id)
            await self._start_voting(room_id, user_id)
            return
        
        # Determine winner
        winner = plandidate_a if choice == "1" else plandidate_b
        
        # Record vote
        self.store.record_vote(
            user_id=user_id,
            plandidate_a_id=plandidate_a.id,
            plandidate_b_id=plandidate_b.id,
            winner_id=winner.id
        )
        
        # Update Elo ratings
        a_won = (choice == "1")
        new_elo_a, new_elo_b = self.elo.update_ratings(
            plandidate_a.elo,
            plandidate_b.elo,
            a_won
        )
        
        self.store.update_plandidate_elo(plandidate_a.id, new_elo_a)
        self.store.update_plandidate_elo(plandidate_b.id, new_elo_b)
        
        # Clear session
        self.store.clear_session(user_id)
        
        # Send confirmation and next pair
        await self._send_message(
            room_id,
            f"✅ Recorded your preference for **{winner.name}**!"
        )
        
        # Continue to next pair
        await self._start_voting(room_id, user_id)
    
    async def _send_message(self, room_id: str, message: str):
        """Send a message to a room."""
        await self.client.room_send(
            room_id=room_id,
            message_type="m.room.message",
            content={
                "msgtype": "m.text",
                "body": message,
                "format": "org.matrix.custom.html",
                "formatted_body": self._markdown_to_html(message)
            }
        )
    
    def _markdown_to_html(self, text: str) -> str:
        """Convert simple markdown to HTML for Matrix."""
        # Simple conversions
        html = text
        
        # Bold: **text** -> <strong>text</strong>
        import re
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        
        # Italic: _text_ -> <em>text</em>
        html = re.sub(r'_(.+?)_', r'<em>\1</em>', html)
        
        # Line breaks
        html = html.replace('\n', '<br/>')
        
        return html
