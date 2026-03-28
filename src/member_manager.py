import csv
from datetime import datetime
from pathlib import Path
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
import json
from src.config import Config
from src.logger import logger

class MemberManager:
    """Manage member data and CSV operations"""
    
    def __init__(self):
        self.output_dir = Config.CSV_OUTPUT_DIR
        
    def save_members_to_csv(self, members: list, filename: str):
        """Save members to CSV with atomic writes (temp file first)"""
        filepath = self.output_dir / f"{filename}.csv"
        temp_filepath = self.output_dir / f"{filename}.csv.tmp"
        
        try:
            # Write to temp file first
            with open(temp_filepath, 'w', newline='', encoding='utf-8') as f:
                if not members:
                    return
                
                fieldnames = members[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(members)
            
            # Atomic move
            temp_filepath.replace(filepath)
            logger.info(f"Saved {len(members)} members to {filepath}")
            
        except Exception as e:
            logger.error(f"Error saving CSV: {e}")
            if temp_filepath.exists():
                temp_filepath.unlink()
            raise
    
    def load_members_from_csv(self, filename: str) -> list:
        """Load members from CSV"""
        filepath = self.output_dir / f"{filename}.csv"
        
        if not filepath.exists():
            logger.warning(f"File not found: {filepath}")
            return []
        
        try:
            members = []
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                members = list(reader)
            
            logger.info(f"Loaded {len(members)} members from {filepath}")
            return members
        except Exception as e:
            logger.error(f"Error reading CSV: {e}")
            return []
    
    def save_checkpoint(self, checkpoint_name: str, data: dict):
        """Save checkpoint for resume functionality"""
        checkpoint_file = self.output_dir / f".checkpoint_{checkpoint_name}.json"
        
        try:
            with open(checkpoint_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Checkpoint saved: {checkpoint_name}")
        except Exception as e:
            logger.error(f"Error saving checkpoint: {e}")
            raise
    
    def load_checkpoint(self, checkpoint_name: str) -> dict:
        """Load checkpoint data"""
        checkpoint_file = self.output_dir / f".checkpoint_{checkpoint_name}.json"
        
        if not checkpoint_file.exists():
            return {}
        
        try:
            with open(checkpoint_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading checkpoint: {e}")
            return {}
    
    def delete_checkpoint(self, checkpoint_name: str):
        """Delete checkpoint"""
        checkpoint_file = self.output_dir / f".checkpoint_{checkpoint_name}.json"
        if checkpoint_file.exists():
            checkpoint_file.unlink()
            logger.info(f"Checkpoint deleted: {checkpoint_name}")
