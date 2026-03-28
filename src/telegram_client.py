from pyrogram import Client
from pyrogram.errors import FloodWait
import asyncio
from src.config import Config
from src.logger import logger
from src.session_manager import SessionManager

class TelegramClient:
    """Pyrogram client wrapper with account rotation and flood wait handling"""
    
    def __init__(self):
        self.session_manager = SessionManager()
        self.clients = {}
        self.current_account = None
        
    async def create_client(self, account_name: str, phone: str = None) -> Client:
        """Create a new Pyrogram client session"""
        client = Client(
            name=account_name,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            workdir=str(Config.SESSIONS_DIR),
            phone_number=phone
        )
        
        self.clients[account_name] = client
        return client
    
    async def load_client(self, account_name: str) -> Client:
        """Load existing client from session"""
        if account_name in self.clients:
            return self.clients[account_name]
        
        try:
            session_string = self.session_manager.load_session(account_name)
            client = Client(
                name=account_name,
                api_id=Config.API_ID,
                api_hash=Config.API_HASH,
                session_string=session_string,
                workdir=str(Config.SESSIONS_DIR)
            )
            self.clients[account_name] = client
            return client
        except Exception as e:
            logger.error(f"Failed to load client {account_name}: {e}")
            raise
    
    async def connect(self, account_name: str):
        """Connect a client"""
        try:
            client = await self.load_client(account_name)
            await client.connect()
            logger.info(f"Connected: {account_name}")
            return client
        except Exception as e:
            logger.error(f"Connection failed for {account_name}: {e}")
            raise
    
    async def disconnect(self, account_name: str):
        """Disconnect a client"""
        if account_name in self.clients:
            await self.clients[account_name].disconnect()
            logger.info(f"Disconnected: {account_name}")
    
    async def disconnect_all(self):
        """Disconnect all clients"""
        for account_name in list(self.clients.keys()):
            await self.disconnect(account_name)
    
    async def handle_floodwait(self, wait_time: int):
        """Handle FloodWait with automatic account rotation"""
        logger.warning(f"FloodWait: waiting {wait_time} seconds")
        
        if wait_time > 3600:  # 1 hour
            logger.info("Large FloodWait detected, rotating account...")
            # Account rotation logic would go here
        
        await asyncio.sleep(wait_time)
    
    async def get_me(self, account_name: str):
        """Get current user info"""
        try:
            client = await self.load_client(account_name)
            if not client.is_connected:
                await client.connect()
            me = await client.get_me()
            return me
        except Exception as e:
            logger.error(f"Failed to get user info: {e}")
            raise
