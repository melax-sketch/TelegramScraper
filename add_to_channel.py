#!/usr/bin/env python3
"""
Direct member adder script for @Skill_share_et channel
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Config
from src.logger import logger
from src.telegram_client import TelegramClient
from src.adder import Adder

async def add_members_to_channel():
    """Add members from CSV to @Skill_share_et channel"""
    
    # Configuration
    ACCOUNT_NAME = "mela1"
    CHANNEL_USERNAME = "@Skill_share_et"
    CSV_FILENAME = "members_Digital_Id_Ethiopia_ፋይዳ"  # Without .csv extension
    
    try:
        print("\n" + "="*60)
        print("ADDING MEMBERS TO @Skill_share_et")
        print("="*60)
        
        # Validate config
        Config.validate()
        print(f"✓ Config validated")
        
        # Initialize client
        telegram_client = TelegramClient()
        print(f"✓ Connecting with account: {ACCOUNT_NAME}...")
        
        client = await telegram_client.connect(ACCOUNT_NAME)
        
        # Get user info
        me = await client.get_me()
        print(f"✓ Connected as: @{me.username} ({me.first_name})")
        
        # Resolve channel
        print(f"✓ Resolving channel: {CHANNEL_USERNAME}...")
        try:
            chat = await client.get_chat(CHANNEL_USERNAME)
            channel_id = chat.id
            print(f"✓ Channel ID: {channel_id}")
            print(f"✓ Channel: {chat.title}")
        except Exception as e:
            print(f"✗ Failed to resolve channel: {e}")
            await telegram_client.disconnect(ACCOUNT_NAME)
            return False
        
        # Initialize adder
        adder = Adder(client)
        
        # Add members (Rush mode)
        print(f"\n📤 Starting to add members...")
        result = await adder.add_members_rush(channel_id, CSV_FILENAME, remove_added=False)
        
        print("\n" + "="*60)
        print("RESULTS:")
        if result:
            print(f"✓ Successfully added: {result['added']} members")
            print(f"✗ Failed: {result['failed']} members")
        else:
            print(f"✗ No members were added")
        print("="*60)
        
        # Disconnect
        await telegram_client.disconnect(ACCOUNT_NAME)
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        logger.error(f"Error: {e}", exc_info=True)
        return False

async def main():
    success = await add_members_to_channel()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())
