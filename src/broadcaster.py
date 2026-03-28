import asyncio
import random
from pyrogram import Client
from pyrogram.errors import FloodWait
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from src.logger import logger
from src.member_manager import MemberManager

class Broadcaster:
    """Send messages to members"""
    
    def __init__(self, client: Client):
        self.client = client
        self.member_manager = MemberManager()
        self.sent = []
        self.failed = []
        
    async def read_broadcast_message(self, markdown_file: str) -> str:
        """Read broadcast message from markdown file"""
        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading broadcast file: {e}")
            raise
    
    async def broadcast_to_members(
        self,
        csv_file: str,
        message_content: str,
        delay_min: int = None,
        delay_max: int = None
    ):
        """Broadcast message to all members with random delays"""
        
        delay_min = delay_min or 30
        delay_max = delay_max or 60
        
        members = self.member_manager.load_members_from_csv(csv_file)
        
        if not members:
            logger.error(f"No members found in {csv_file}")
            return
        
        self.sent = []
        self.failed = []
        
        with Progress(
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task(
                "[cyan]Broadcasting messages...",
                total=len(members)
            )
            
            for member in members:
                try:
                    user_id = int(member["user_id"])
                    
                    # Send message
                    await self.client.send_message(user_id, message_content)
                    self.sent.append(member)
                    
                    # Random delay between requests
                    delay = random.randint(delay_min, delay_max)
                    await asyncio.sleep(delay)
                    
                except FloodWait as fw:
                    logger.warning(f"FloodWait: {fw.value}s")
                    await asyncio.sleep(fw.value)
                    
                except Exception as e:
                    self.failed.append({"member": member, "error": str(e)})
                    logger.debug(f"Failed to send message to {member.get('username', 'unknown')}: {e}")
                
                finally:
                    progress.advance(task)
                    progress.update(
                        task,
                        description=f"[cyan]Sent: {len(self.sent)} | Failed: {len(self.failed)}"
                    )
        
        logger.info(f"Broadcast complete: {len(self.sent)} sent, {len(self.failed)} failed")
        return {"sent": len(self.sent), "failed": len(self.failed)}
