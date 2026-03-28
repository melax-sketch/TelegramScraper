import asyncio
from pyrogram import Client
from pyrogram.types import ChatMember
from pyrogram.errors import FloodWait, PeerIdInvalid, ChannelPrivate
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from src.logger import logger
from src.member_manager import MemberManager

class Scraper:
    """Telegram group member scraper"""
    
    def __init__(self, client: Client):
        self.client = client
        self.member_manager = MemberManager()
    
    async def resolve_group(self, group_identifier: str):
        """Resolve group ID or username to chat ID"""
        try:
            # Try to parse as integer
            if group_identifier.startswith('-'):
                chat_id = int(group_identifier)
            elif group_identifier.startswith('@'):
                # Get chat by username
                chat = await self.client.get_chat(group_identifier)
                chat_id = chat.id
            else:
                try:
                    chat_id = int(group_identifier)
                except ValueError:
                    # Treat as username
                    chat = await self.client.get_chat(f"@{group_identifier}")
                    chat_id = chat.id
            return chat_id
        except Exception as e:
            logger.error(f"Failed to resolve group: {e}")
            raise
        
    async def scrape_visible_members(self, group_identifier: str, output_file: str):
        """Scrape members from visible members list"""
        members = []
        
        try:
            # Resolve group ID
            group_id = await self.resolve_group(group_identifier)
            logger.info(f"Resolved group to ID: {group_id}")
            
            with Progress(
                SpinnerColumn(),
                BarColumn(),
                TextColumn("[progress.description]{task.description}"),
            ) as progress:
                task = progress.add_task("[cyan]Scraping visible members...", total=None)
                
                try:
                    async for member in self.client.get_chat_members(group_id):
                        if member.user:
                            members.append({
                                "user_id": str(member.user.id),
                                "username": member.user.username or "N/A",
                                "first_name": member.user.first_name or "",
                                "last_name": member.user.last_name or "",
                                "is_bot": member.user.is_bot,
                                "status": str(member.status),
                            })
                        
                        if len(members) % 100 == 0:
                            progress.update(
                                task,
                                description=f"[cyan]Scraped {len(members)} members..."
                            )
                            await asyncio.sleep(0.1)  # Small delay to prevent flooding
                except FloodWait as fw:
                    logger.warning(f"FloodWait: {fw.value}s")
                    await asyncio.sleep(fw.value)
                    raise
            
            # Save to CSV
            if members:
                self.member_manager.save_members_to_csv(members, output_file)
                logger.info(f"Successfully scraped {len(members)} members")
            else:
                logger.warning("No members found in group")
            
            return members
            
        except (ChannelPrivate, PeerIdInvalid) as e:
            logger.error(f"Cannot access group - it may be private or invalid: {e}")
            raise ValueError("Group is private or invalid. Make sure you're a member and the group exists.")
        except Exception as e:
            logger.error(f"Error scraping visible members: {e}")
            raise
    
    async def scrape_hidden_members(self, group_identifier: str, output_file: str, limit: int = None):
        """Scrape members from message history (hidden members)"""
        members = {}
        
        try:
            # Resolve group ID
            group_id = await self.resolve_group(group_identifier)
            logger.info(f"Resolved group to ID: {group_id}")
            
            with Progress(
                SpinnerColumn(),
                BarColumn(),
                TextColumn("[progress.description]{task.description}"),
            ) as progress:
                task = progress.add_task("[cyan]Scraping hidden members...", total=None)
                
                try:
                    async for message in self.client.get_chat_history(group_id, limit=limit or 100000):
                        if message.from_user:
                            user = message.from_user
                            user_id = user.id
                            
                            if user_id not in members:
                                members[user_id] = {
                                    "user_id": str(user_id),
                                    "username": user.username or "N/A",
                                    "first_name": user.first_name or "",
                                    "last_name": user.last_name or "",
                                    "is_bot": user.is_bot,
                                    "status": "member",
                                }
                        
                        if len(members) % 100 == 0:
                            progress.update(
                                task,
                                description=f"[cyan]Found {len(members)} unique members..."
                            )
                            await asyncio.sleep(0.1)
                except FloodWait as fw:
                    logger.warning(f"FloodWait: {fw.value}s")
                    await asyncio.sleep(fw.value)
                    raise
            
            # Convert to list and save
            members_list = list(members.values())
            if members_list:
                self.member_manager.save_members_to_csv(members_list, output_file)
                logger.info(f"Successfully found {len(members_list)} hidden members")
            else:
                logger.warning("No members found in message history")
            
            return members_list
            
        except (ChannelPrivate, PeerIdInvalid) as e:
            logger.error(f"Cannot access group - it may be private or invalid: {e}")
            raise ValueError("Group is private or invalid. Make sure you're a member and the group exists.")
        except Exception as e:
            logger.error(f"Error scraping hidden members: {e}")
            raise
    
    async def get_group_info(self, group_identifier: str):
        """Get group information"""
        try:
            # Resolve group ID first
            group_id = await self.resolve_group(group_identifier)
            
            chat = await self.client.get_chat(group_id)
            return {
                "id": chat.id,
                "title": chat.title or "Unknown",
                "type": str(chat.type) if chat.type else "Unknown",
                "members_count": chat.members_count or "Unknown",
                "description": chat.description or "N/A",
            }
        except (ChannelPrivate, PeerIdInvalid) as e:
            logger.error(f"Cannot access group: {e}")
            raise ValueError("Group is private or invalid")
        except Exception as e:
            logger.error(f"Error getting group info: {e}")
            raise
