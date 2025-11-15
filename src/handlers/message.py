"""Message event handlers."""

from nio import AsyncClient, RoomMessageText

from storage import JSONStore
from ranking import EloRanking
from commands import AddCommand, RevealCommand, ResetCommand
from handlers.dm import DMHandler
from config import Terminology


class MessageHandler:
    """Handle incoming Matrix messages."""
    
    def __init__(self, client: AsyncClient, store: JSONStore, elo: EloRanking, bot_user_id: str):
        self.client = client
        self.store = store
        self.bot_user_id = bot_user_id
        
        # Extract bot localpart for mentions
        self.bot_name = bot_user_id.split(':')[0].lstrip('@')
        
        # Initialize command handlers
        self.add_command = AddCommand(store)
        self.reveal_command = RevealCommand(store)
        self.reset_command = ResetCommand(store)
        
        # Initialize DM handler
        self.dm_handler = DMHandler(client, store, elo)
        
        # Track processed events to avoid duplicates
        self.processed_events = set()
        self.max_processed_events = 1000  # Prevent memory leak
    
    async def handle_message(self, room, event: RoomMessageText):
        """
        Handle a room message event.
        
        Args:
            room: The room object
            event: The message event
        """
        # Ignore messages from the bot itself
        if event.sender == self.bot_user_id:
            return
        
        # Security check: only respond to allowed users
        from config import Config
        if not Config.is_user_allowed(event.sender):
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Ignoring message from unauthorized user: {event.sender}")
            return
        
        # Deduplicate events by event_id
        event_id = event.event_id
        if event_id in self.processed_events:
            return
        
        # Add to processed set
        self.processed_events.add(event_id)
        
        # Keep the set from growing unbounded
        if len(self.processed_events) > self.max_processed_events:
            # Remove oldest half
            self.processed_events = set(list(self.processed_events)[self.max_processed_events // 2:])
        
        message = event.body
        sender = event.sender
        room_id = room.room_id
        
        # Check if bot is mentioned (priority over DM detection)
        bot_mentioned = f"@{self.bot_name}" in message or self.bot_user_id in message
        
        if bot_mentioned:
            # Handle as a command (even in DM)
            await self._handle_command(room_id, sender, message)
        else:
            # Check if this is a DM (room with only 2 members: bot and user)
            members = room.member_count
            is_dm = members == 2
            
            if is_dm:
                # Handle DM voting
                await self.dm_handler.handle_dm(room_id, sender, message)
    
    async def _handle_command(self, room_id: str, sender: str, message: str):
        """
        Handle a command in a public room.
        
        Args:
            room_id: The room ID
            sender: The sender's user ID
            message: The message content
        """
        response = None
        
        # Debug logging
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Processing command from {sender}: {message}")
        logger.info(f"Bot name: {self.bot_name}")
        
        # Try reset all command
        if self.reset_command.parse_reset_all_command(message, self.bot_name):
            logger.info(f"Parsed reset all command")
            response = self.reset_command.execute_reset_all()
        
        # Try rerank command
        elif self.reset_command.parse_rerank_command(message, self.bot_name):
            logger.info(f"Parsed rerank command")
            response = self.reset_command.execute_rerank()
        
        # Try add command
        elif (plandidate_name := self.add_command.parse_command(message, self.bot_name)):
            logger.info(f"Parsed add command with plandidate: {plandidate_name}")
            response = self.add_command.execute(plandidate_name, sender)
        
        # Try reveal command
        elif self.reveal_command.parse_command(message, self.bot_name):
            logger.info(f"Parsed reveal command")
            response = self.reveal_command.execute()
        
        # Help message if bot mentioned but no command recognized
        else:
            response = self._get_help_message()
        
        if response:
            await self._send_message(room_id, response)
    
    def _get_help_message(self) -> str:
        """Get the help message."""
        return Terminology.get('messages.help_text', bot_name=self.bot_name)
    
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
        import re
        html = text
        
        # Bold: **text** -> <strong>text</strong>
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        
        # Italic: _text_ -> <em>text</em>
        html = re.sub(r'_(.+?)_', r'<em>\1</em>', html)
        
        # Code: `text` -> <code>text</code>
        html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
        
        # Bullet points: • or - at start of line
        html = re.sub(r'^[•\-]\s', r'• ', html, flags=re.MULTILINE)
        
        # Line breaks
        html = html.replace('\n', '<br/>')
        
        return html
