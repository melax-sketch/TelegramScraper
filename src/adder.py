import asyncio
from pyrogram import Client
from pyrogram.errors import FloodWait, UsernameInvalid
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from src.logger import logger
from src.member_manager import MemberManager

class Adder:
    """Telegram member adder"""
    
    def __init__(self, client: Client):
        self.client = client
        self.member_manager = MemberManager()
        self.added = []
        self.failed = []
        
    async def add_members_rush(self, group_id: int, csv_file: str, remove_added: bool = True):
        """
        Rush Adder: Fast adding with progress tracking.
        Optionally removes added members from CSV.
        """
        members = self.member_manager.load_members_from_csv(csv_file)
        
        if not members:
            logger.error(f"No members found in {csv_file}")
            return
        
        self.added = []
        self.failed = []
        
        with Progress(
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task(
                "[cyan]Adding members (Rush mode)...",
                total=len(members)
            )
            
            for member in members:
                try:
                    user_id = int(member["user_id"])
                    
                    await self.client.add_chat_members(group_id, user_id)
                    self.added.append(member)
                    
                except FloodWait as fw:
                    logger.warning(f"FloodWait: {fw.value}s")
                    await asyncio.sleep(fw.value)
                    
                except Exception as e:
                    self.failed.append({"member": member, "error": str(e)})
                    logger.debug(f"Failed to add {member.get('username', 'unknown')}: {e}")
                
                finally:
                    progress.advance(task)
                    progress.update(
                        task,
                        description=f"[cyan]Added: {len(self.added)} | Failed: {len(self.failed)}"
                    )
        
        # Remove added members from CSV if requested
        if remove_added and self.added:
            remaining = [m for m in members if m not in self.added]
            self.member_manager.save_members_to_csv(remaining, csv_file)
        
        logger.info(f"Rush add complete: {len(self.added)} added, {len(self.failed)} failed")
        return {"added": len(self.added), "failed": len(self.failed)}
    
    async def add_members_calm(self, group_id: int, csv_file: str, delay: int = 3):
        """
        Calm Adder: Slower adding with delays between requests.
        Keeps CSV intact, tracks separately.
        """
        members = self.member_manager.load_members_from_csv(csv_file)
        
        if not members:
            logger.error(f"No members found in {csv_file}")
            return
        
        self.added = []
        self.failed = []
        
        with Progress(
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task(
                "[cyan]Adding members (Calm mode)...",
                total=len(members)
            )
            
            for member in members:
                try:
                    user_id = int(member["user_id"])
                    
                    await self.client.add_chat_members(group_id, user_id)
                    self.added.append(member)
                    
                    # Calm delay between requests
                    await asyncio.sleep(delay)
                    
                except FloodWait as fw:
                    logger.warning(f"FloodWait: {fw.value}s")
                    await asyncio.sleep(fw.value)
                    
                except Exception as e:
                    self.failed.append({"member": member, "error": str(e)})
                    logger.debug(f"Failed to add {member.get('username', 'unknown')}: {e}")
                
                finally:
                    progress.advance(task)
                    progress.update(
                        task,
                        description=f"[cyan]Added: {len(self.added)} | Failed: {len(self.failed)}"
                    )
        
        # Save tracking file separately
        self.member_manager.save_checkpoint(f"added_{csv_file}", {
            "added": self.added,
            "failed": self.failed
        })
        
        logger.info(f"Calm add complete: {len(self.added)} added, {len(self.failed)} failed")
        return {"added": len(self.added), "failed": len(self.failed)}
