#!/usr/bin/env python3
"""
TelegramScraper - Main entry point
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Config
from src.logger import logger
from src.ui import UI
from src.session_manager import SessionManager
from src.telegram_client import TelegramClient
from src.scraper import Scraper
from src.adder import Adder
from src.broadcaster import Broadcaster


class TelegramScraperApp:
    """Main application"""
    
    def __init__(self):
        self.session_manager = SessionManager()
        self.telegram_client = TelegramClient()
        self.ui = UI
        
    async def login_account(self):
        """Login to Telegram account"""
        self.ui.show_info("Starting login process...")
        
        account_name = self.ui.prompt_account_name("Enter account name for this login")
        phone = self.ui.prompt_phone()
        
        try:
            client = await self.telegram_client.create_client(account_name, phone)
            
            self.ui.show_info("Connecting to Telegram...")
            await client.connect()
            
            self.ui.show_info("Sending OTP...")
            sent_code = await client.send_code(phone)
            
            # Prompt for OTP with retry
            max_attempts = 3
            for attempt in range(max_attempts):
                otp = self.ui.prompt_account_name(f"Enter OTP code (Attempt {attempt+1}/{max_attempts})")
                
                try:
                    self.ui.show_info("Verifying code...")
                    await client.sign_in(phone, sent_code.phone_code_hash, otp)
                    break
                except Exception as e:
                    if attempt < max_attempts - 1:
                        self.ui.show_warning(f"Code invalid. Try again. Error: {str(e)}")
                    else:
                        raise
            
            # Get user info
            me = await client.get_me()
            
            # Save session
            session_string = await client.export_session_string()
            self.session_manager.save_session(account_name, session_string, phone)
            
            await client.disconnect()
            
            self.ui.show_success(f"Successfully logged in as @{me.username}")
            
        except Exception as e:
            self.ui.show_error(f"Login failed: {e}")
            logger.error(f"Login error: {e}", exc_info=True)
    
    async def manage_sessions(self):
        """Manage saved sessions"""
        while True:
            sessions = self.session_manager.list_sessions()
            self.ui.show_info(f"Total sessions: {len(sessions)}")
            
            if sessions:
                self.ui.show_sessions_table(sessions)
            
            self.ui.show_main_menu()
            choice = input("\n[cyan]Select session to manage (or 'back' to return)[/cyan]: ").strip()
            
            if choice.lower() == 'back':
                break
            
            if choice in sessions:
                await self.session_menu(choice)
    
    async def session_menu(self, account_name: str):
        """Menu for single session"""
        menu_options = {
            "1": ("Test Connection", self.test_session),
            "2": ("Delete Session", self.delete_session),
            "3": ("Export Session", self.export_session),
        }
        
        while True:
            self.ui.show_info(f"Session: {account_name}")
            
            for code, (desc, _) in menu_options.items():
                print(f"{code}. {desc}")
            
            choice = input("\nSelect option (or 'back'): ").strip()
            
            if choice == 'back':
                break
            
            if choice in menu_options:
                await menu_options[choice][1](account_name)
    
    async def test_session(self, account_name: str):
        """Test session connectivity"""
        try:
            self.ui.show_info(f"Testing {account_name}...")
            me = await self.telegram_client.get_me(account_name)
            self.ui.show_success(f"✓ Connected as @{me.username} ({me.first_name})")
        except Exception as e:
            self.ui.show_error(f"Connection failed: {e}")
    
    async def delete_session(self, account_name: str):
        """Delete a session"""
        if self.ui.confirm(f"Delete {account_name}? This cannot be undone."):
            self.session_manager.delete_session(account_name)
            self.ui.show_success(f"Session deleted: {account_name}")
    
    async def export_session(self, account_name: str):
        """Export session string (for backup)"""
        try:
            session = self.session_manager.load_session(account_name)
            # In production, only show first/last chars for security
            self.ui.show_info(f"Session (encrypted): {session[:10]}...{session[-10:]}")
        except Exception as e:
            self.ui.show_error(f"Error: {e}")
    
    async def scrape_members(self):
        """Scrape group members"""
        account_name = self.ui.prompt_account_name("Select account to use")
        group_identifier = self.ui.prompt_group_id()
        
        if not group_identifier:
            self.ui.show_error("No group specified")
            return
        
        print("\n[cyan]Scraping mode:[/cyan]")
        print("1. Visible members (from member list)")
        print("2. Hidden members (from message history)")
        
        mode = input("Select mode (1 or 2): ").strip()
        
        if mode not in ["1", "2"]:
            self.ui.show_error("Invalid scraping mode")
            return
        
        try:
            self.ui.show_info(f"Connecting with account: {account_name}...")
            client = await self.telegram_client.connect(account_name)
            scraper = Scraper(client)
            
            # Get group info
            self.ui.show_info(f"Resolving group: {group_identifier}...")
            group_info = await scraper.get_group_info(group_identifier)
            self.ui.show_success(f"Group: {group_info['title']}")
            self.ui.show_info(f"Type: {group_info['type']} | Members: {group_info['members_count']}")
            
            # Sanitize output filename
            safe_name = group_info.get('title', 'group').replace(' ', '_').replace('/', '_')
            output_file = f"members_{safe_name}"
            
            if mode == "1":
                self.ui.show_info("Starting visible members scrape...")
                members = await scraper.scrape_visible_members(group_identifier, output_file)
                self.ui.show_success(f"Scraped {len(members)} visible members")
            else:
                self.ui.show_info("Starting hidden members scrape...")
                members = await scraper.scrape_hidden_members(group_identifier, output_file)
                self.ui.show_success(f"Found {len(members)} unique members in message history")
            
            self.ui.show_success(f"✓ Members saved to: output/{output_file}.csv")
            
            await self.telegram_client.disconnect(account_name)
            
        except ValueError as e:
            self.ui.show_error(f"Validation error: {e}")
            logger.error(f"Validation error: {e}")
        except Exception as e:
            self.ui.show_error(f"Scraping failed: {str(e)}")
            logger.error(f"Scraping error: {e}", exc_info=True)
    
    async def add_members(self):
        """Add members to group"""
        account_name = self.ui.prompt_account_name("Select account to use")
        group_id = self.ui.prompt_group_id()
        csv_file = self.ui.prompt_csv_file()
        
        if not group_id:
            return
        
        print("\nAdding mode:")
        print("1. Rush Adder (fast, removes added from CSV)")
        print("2. Calm Adder (slow with delays, keeps CSV intact)")
        
        mode = input("Select mode (1 or 2): ").strip()
        
        try:
            client = await self.telegram_client.connect(account_name)
            adder = Adder(client)
            
            if mode == "1":
                result = await adder.add_members_rush(group_id, csv_file)
            elif mode == "2":
                result = await adder.add_members_calm(group_id, csv_file)
            else:
                self.ui.show_error("Invalid option")
                return
            
            await self.telegram_client.disconnect(account_name)
            self.ui.show_success(f"Adding completed: {result['added']} added, {result['failed']} failed")
            
        except Exception as e:
            self.ui.show_error(f"Adding failed: {e}")
            logger.error(f"Adding error: {e}", exc_info=True)
    
    async def broadcast_message(self):
        """Broadcast message to members"""
        account_name = self.ui.prompt_account_name("Select account to use")
        csv_file = self.ui.prompt_csv_file()
        
        markdown_file = input("Enter markdown file path: ").strip()
        
        try:
            client = await self.telegram_client.connect(account_name)
            broadcaster = Broadcaster(client)
            
            self.ui.show_info("Reading message...")
            message = await broadcaster.read_broadcast_message(markdown_file)
            
            if self.ui.confirm(f"Broadcast to members in {csv_file}?"):
                result = await broadcaster.broadcast_to_members(csv_file, message)
                self.ui.show_success(f"Broadcast completed: {result['sent']} sent, {result['failed']} failed")
            
            await self.telegram_client.disconnect(account_name)
            
        except Exception as e:
            self.ui.show_error(f"Broadcast failed: {e}")
            logger.error(f"Broadcast error: {e}", exc_info=True)
    
    async def run(self):
        """Main application loop"""
        try:
            Config.validate()
        except ValueError as e:
            logger.error(str(e))
            print(f"\n[red]Error: {e}[/red]")
            print("[yellow]Please set API_ID and API_HASH in .env file[/yellow]")
            return
        
        while True:
            print("\n" + "="*50)
            self.ui.show_banner()
            
            sessions = self.session_manager.list_sessions()
            self.ui.show_info(f"{len(sessions)} sessions loaded")
            
            self.ui.show_main_menu()
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "01":
                await self.login_account()
            elif choice == "02":
                await self.manage_sessions()
            elif choice == "03":
                await self.scrape_members()
            elif choice == "04":
                await self.add_members()
            elif choice == "05":
                await self.broadcast_message()
            elif choice == "06":
                self.ui.show_info("Logs are saved in ./logs directory")
            elif choice == "07":
                self.ui.show_info("Exiting...")
                await self.telegram_client.disconnect_all()
                break
            else:
                self.ui.show_error("Invalid option")


async def main():
    """Entry point"""
    app = TelegramScraperApp()
    await app.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n[yellow]Interrupted by user[/yellow]")
        sys.exit(0)
