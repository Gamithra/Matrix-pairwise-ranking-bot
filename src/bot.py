#!/usr/bin/env python3
"""
Planter Bot - A Matrix bot for ranking plandidates using pairwise comparisons.
"""

import asyncio
import logging
import sys

from nio import (
    AsyncClient,
    AsyncClientConfig,
    RoomMessageText,
    LoginError,
    SyncError
)

from config import Config
from storage import JSONStore
from ranking import EloRanking
from handlers import MessageHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class PlanterBot:
    """Main bot class."""
    
    def __init__(self):
        """Initialize the bot."""
        # Validate configuration
        Config.validate()
        
        # Initialize storage
        self.store = JSONStore(Config.DATA_DIR)
        
        # Initialize Elo ranking
        self.elo = EloRanking(k_factor=32.0)
        
        # Track when bot started - only respond to messages after this
        self.start_time = None
        self.ready = False
        
        # Initialize Matrix client
        client_config = AsyncClientConfig(
            store_sync_tokens=True,
            encryption_enabled=False,  # Simplified - enable if needed
        )
        
        self.client = AsyncClient(
            homeserver=Config.HOMESERVER,
            user=Config.USER_ID,
            config=client_config,
            store_path=Config.STORE_DIR
        )
        
        # Initialize message handler
        self.message_handler = MessageHandler(
            self.client,
            self.store,
            self.elo,
            Config.USER_ID
        )
        
        # Register callbacks
        self.client.add_event_callback(self._handle_message, RoomMessageText)
    
    async def _handle_message(self, room, event: RoomMessageText):
        """Callback for message events."""
        try:
            # Only process messages after bot is ready (after initial sync)
            if not self.ready:
                logger.debug(f"Ignoring old message {event.event_id} (bot not ready yet)")
                return
            
            # Only process messages sent after the bot started
            if self.start_time and event.server_timestamp < self.start_time:
                logger.debug(f"Ignoring old message {event.event_id} (timestamp {event.server_timestamp} < start {self.start_time})")
                return
            
            logger.info(f"Received event {event.event_id} in room {room.room_id} from {event.sender}")
            await self.message_handler.handle_message(room, event)
        except Exception as e:
            logger.error(f"Error handling message: {e}", exc_info=True)
    
    async def login(self):
        """Log in to Matrix."""
        logger.info(f"Logging in as {Config.USER_ID}...")
        logger.info(f"Connecting to homeserver: {Config.HOMESERVER}")
        
        # Use access token if provided, otherwise use password
        if Config.ACCESS_TOKEN:
            logger.info("Using access token authentication")
            self.client.access_token = Config.ACCESS_TOKEN
            self.client.user_id = Config.USER_ID
            
            # Verify the token works by doing a simple sync
            try:
                sync_response = await self.client.sync(timeout=1000)
                if isinstance(sync_response, SyncError):
                    logger.error(f"Failed to authenticate with access token: {sync_response.message}")
                    return False
                logger.info("Access token authentication successful!")
            except Exception as e:
                logger.error(f"Failed to authenticate with access token: {e}")
                return False
        else:
            logger.info("Using password authentication")
            # Try login with device name
            response = await self.client.login(
                password=Config.PASSWORD,
                device_name="PlanterBot"
            )
            
            if isinstance(response, LoginError):
                logger.error(f"Failed to log in: {response.message}")
                logger.error(f"Error status code: {response.status_code}")
                logger.error(f"Please verify your credentials in .env:")
                logger.error(f"  - MATRIX_HOMESERVER is correct")
                logger.error(f"  - MATRIX_USER_ID matches exactly (e.g., @user:homeserver)")
                logger.error(f"  - MATRIX_PASSWORD is correct (check for special characters)")
                return False
            
            logger.info("Login successful!")
        
        # Set display name if configured
        if Config.DISPLAY_NAME:
            await self.client.set_displayname(Config.DISPLAY_NAME)
        
        return True
    
    async def sync_forever(self):
        """Sync messages forever."""
        logger.info("Starting sync loop...")
        
        # Record start time (in milliseconds since epoch, like Matrix timestamps)
        import time
        self.start_time = int(time.time() * 1000)
        
        # Initial sync to get current state (don't respond to old messages)
        sync_response = await self.client.sync(timeout=30000, full_state=True)
        
        if isinstance(sync_response, SyncError):
            logger.error(f"Initial sync failed: {sync_response.message}")
            return
        
        # Mark bot as ready - now we'll respond to new messages
        self.ready = True
        logger.info("Initial sync complete. Bot is ready and will respond to new messages!")
        
        # Sync loop
        while True:
            try:
                sync_response = await self.client.sync(timeout=30000)
                
                if isinstance(sync_response, SyncError):
                    logger.error(f"Sync error: {sync_response.message}")
                    await asyncio.sleep(5)
                    continue
                
            except Exception as e:
                logger.error(f"Sync loop error: {e}", exc_info=True)
                await asyncio.sleep(5)
    
    async def run(self):
        """Run the bot."""
        try:
            # Login
            if not await self.login():
                logger.error("Failed to login. Exiting.")
                return
            
            # Sync forever
            await self.sync_forever()
            
        except KeyboardInterrupt:
            logger.info("Received interrupt, shutting down...")
        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)
        finally:
            # Cleanup
            await self.client.close()
    
    async def close(self):
        """Clean up resources."""
        await self.client.close()


async def main():
    """Main entry point."""
    bot = PlanterBot()
    await bot.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
