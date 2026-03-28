"""
Telegram Management Bot for TelegramScraper
This bot allows remote control of the scraper via Telegram commands
"""

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from src.config import Config
from src.logger import logger
from src.telegram_client import TelegramClient
from src.scraper import Scraper
from src.adder import Adder
import os

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))  # Your Telegram user ID

class ManagingBot:
    """Telegram bot for managing scraper operations"""
    
    def __init__(self):
        self.bot = Client(
            "management_bot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=BOT_TOKEN,
            workdir=str(Config.SESSIONS_DIR)
        )
        
        self.telegram_client = TelegramClient()
        self.register_handlers()
        
    def register_handlers(self):
        """Register bot command handlers"""
        
        @self.bot.on_message(filters.command("start") & filters.private)
        async def start_handler(client: Client, message: Message):
            await self.start(client, message)
        
        @self.bot.on_message(filters.command("help") & filters.private)
        async def help_handler(client: Client, message: Message):
            await self.help_command(client, message)
        
        @self.bot.on_message(filters.command("status") & filters.private)
        async def status_handler(client: Client, message: Message):
            await self.status_command(client, message)
        
        @self.bot.on_message(filters.command("scrape") & filters.private)
        async def scrape_handler(client: Client, message: Message):
            await self.scrape_command(client, message)
        
        @self.bot.on_message(filters.command("add") & filters.private)
        async def add_handler(client: Client, message: Message):
            await self.add_command(client, message)
        
        @self.bot.on_message(filters.command("sessions") & filters.private)
        async def sessions_handler(client: Client, message: Message):
            await self.sessions_command(client, message)
    
    async def start(self, client: Client, message: Message):
        """Handle /start command"""
        if message.from_user.id != OWNER_ID:
            await message.reply_text("❌ Unauthorized. Only owner can use this bot.")
            return
        
        welcome_text = """
🤖 **TelegramScraper Management Bot**

I can help you manage scraping operations remotely.

Use /help for available commands.
        """
        await message.reply_text(welcome_text)
    
    async def help_command(self, client: Client, message: Message):
        """Show available commands"""
        if message.from_user.id != OWNER_ID:
            await message.reply_text("❌ Unauthorized.")
            return
        
        help_text = """
📖 **Available Commands:**

**Scraping:**
• /scrape <account> <group_id> - Scrape visible members
• /scrape_hidden <account> <group_id> - Scrape from message history

**Members:**
• /add <account> <channel_id> <csv_file> - Add members to channel
• /sessions - List all saved sessions
• /status - Show current status

**Info:**
• /help - Show this message
• /start - Start bot

**Example:**
`/scrape mela1 @mygroup` - Scrape members from @mygroup using mela1 account
`/add mela1 -1001234567890 members.csv` - Add members to channel
        """
        await message.reply_text(help_text)
    
    async def status_command(self, client: Client, message: Message):
        """Show bot status"""
        if message.from_user.id != OWNER_ID:
            await message.reply_text("❌ Unauthorized.")
            return
        
        try:
            Config.validate()
            status = "✅ All systems operational\n\n"
            status += f"📁 Sessions: {Config.SESSIONS_DIR}\n"
            status += f"📊 Output: {Config.CSV_OUTPUT_DIR}\n"
            status += f"📝 Logs: {Config.LOG_DIR}\n"
            await message.reply_text(status)
        except Exception as e:
            await message.reply_text(f"❌ Error: {e}")
    
    async def scrape_command(self, client: Client, message: Message):
        """Scrape members from a group"""
        if message.from_user.id != OWNER_ID:
            await message.reply_text("❌ Unauthorized.")
            return
        
        try:
            args = message.text.split()
            if len(args) < 3:
                await message.reply_text("Usage: /scrape <account> <group_id>")
                return
            
            account = args[1]
            group_id = args[2]
            
            await message.reply_text("⏳ Starting scrape...")
            
            # Connect and scrape
            telegram_client = await self.telegram_client.connect(account)
            scraper = Scraper(telegram_client)
            
            # Get group info
            group_info = await scraper.get_group_info(group_id)
            safe_name = group_info.get('title', 'group').replace(' ', '_')
            
            members = await scraper.scrape_visible_members(group_id, f"scrape_{safe_name}")
            
            await self.telegram_client.disconnect(account)
            
            await message.reply_text(
                f"✅ Scraping complete!\n\n"
                f"Group: {group_info['title']}\n"
                f"Members: {len(members)}\n"
                f"File: scrape_{safe_name}.csv"
            )
        
        except Exception as e:
            logger.error(f"Scrape error: {e}")
            await message.reply_text(f"❌ Error: {str(e)[:200]}")
    
    async def add_command(self, client: Client, message: Message):
        """Add members to a channel"""
        if message.from_user.id != OWNER_ID:
            await message.reply_text("❌ Unauthorized.")
            return
        
        try:
            args = message.text.split()
            if len(args) < 4:
                await message.reply_text("Usage: /add <account> <channel_id> <csv_file>")
                return
            
            account = args[1]
            channel_id = args[2]
            csv_file = args[3]
            
            await message.reply_text("⏳ Starting to add members...")
            
            # Connect and add
            telegram_client = await self.telegram_client.connect(account)
            adder = Adder(telegram_client)
            
            result = await adder.add_members_rush(int(channel_id), csv_file, remove_added=False)
            
            await self.telegram_client.disconnect(account)
            
            if result:
                await message.reply_text(
                    f"✅ Adding complete!\n\n"
                    f"Added: {result['added']}\n"
                    f"Failed: {result['failed']}"
                )
            else:
                await message.reply_text("❌ No members were added")
        
        except Exception as e:
            logger.error(f"Add error: {e}")
            await message.reply_text(f"❌ Error: {str(e)[:200]}")
    
    async def sessions_command(self, client: Client, message: Message):
        """List all saved sessions"""
        if message.from_user.id != OWNER_ID:
            await message.reply_text("❌ Unauthorized.")
            return
        
        try:
            from src.session_manager import SessionManager
            sm = SessionManager()
            sessions = sm.list_sessions()
            
            if not sessions:
                await message.reply_text("No sessions found")
                return
            
            session_text = "📱 **Saved Sessions:**\n\n"
            for i, session in enumerate(sessions, 1):
                session_text += f"{i}. {session}\n"
            
            await message.reply_text(session_text)
        
        except Exception as e:
            await message.reply_text(f"❌ Error: {e}")
    
    async def run(self):
        """Start the bot"""
        await self.bot.start()
        logger.info("Management bot started")
        await self.bot.idle()
    
    async def stop(self):
        """Stop the bot"""
        await self.bot.stop()
        logger.info("Management bot stopped")


async def main():
    """Start management bot"""
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not set in environment")
        print("Set BOT_TOKEN in .env: BOT_TOKEN=your_bot_token_from_botfather")
        return
    
    if OWNER_ID == 0:
        print("❌ OWNER_ID not set in environment")
        print("Set OWNER_ID in .env: OWNER_ID=your_telegram_user_id")
        return
    
    try:
        Config.validate()
    except ValueError as e:
        print(f"❌ Config error: {e}")
        return
    
    bot = ManagingBot()
    await bot.run()


if __name__ == "__main__":
    asyncio.run(main())
