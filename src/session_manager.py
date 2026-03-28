import json
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import hashlib
import base64
from src.config import Config
from src.logger import logger

class SessionManager:
    """Manage encrypted Telegram sessions"""
    
    def __init__(self):
        self.sessions_dir = Config.SESSIONS_DIR
        self.sessions_file = self.sessions_dir / "sessions.json"
        self.cipher = self._get_cipher()
        
    def _get_cipher(self) -> Fernet:
        """Get cipher for session encryption"""
        # Derive key from password using SHA256
        password = Config.SESSION_PASSWORD.encode()
        salt = b'telegram_scraper_salt_v1'
        
        # Derive key using PBKDF2-like approach
        derived = password + salt
        for _ in range(100000):
            derived = hashlib.sha256(derived).digest()
        
        key = base64.urlsafe_b64encode(derived)
        return Fernet(key)
    
    def encrypt_session(self, session_string: str) -> str:
        """Encrypt session string using Fernet"""
        encrypted = self.cipher.encrypt(session_string.encode())
        return encrypted.decode()
    
    def decrypt_session(self, encrypted_session: str) -> str:
        """Decrypt session string"""
        try:
            decrypted = self.cipher.decrypt(encrypted_session.encode())
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Failed to decrypt session: {e}")
            raise
    
    def save_session(self, account_name: str, session_string: str, phone: str = ""):
        """Save encrypted session to file"""
        sessions = self._load_sessions()
        
        sessions[account_name] = {
            "session": self.encrypt_session(session_string),
            "phone": phone,
            "created_at": str(Path(self.sessions_file).stat().st_mtime if self.sessions_file.exists() else 0)
        }
        
        with open(self.sessions_file, 'w') as f:
            json.dump(sessions, f, indent=2)
        
        logger.info(f"Session saved: {account_name}")
    
    def load_session(self, account_name: str) -> str:
        """Load and decrypt session string"""
        sessions = self._load_sessions()
        
        if account_name not in sessions:
            raise ValueError(f"Session not found: {account_name}")
        
        encrypted_session = sessions[account_name]["session"]
        return self.decrypt_session(encrypted_session)
    
    def list_sessions(self) -> list:
        """List all available sessions"""
        sessions = self._load_sessions()
        return list(sessions.keys())
    
    def delete_session(self, account_name: str):
        """Delete a session"""
        sessions = self._load_sessions()
        
        if account_name in sessions:
            del sessions[account_name]
            with open(self.sessions_file, 'w') as f:
                json.dump(sessions, f, indent=2)
            logger.info(f"Session deleted: {account_name}")
        else:
            logger.warning(f"Session not found: {account_name}")
    
    def _load_sessions(self) -> dict:
        """Load all sessions from file"""
        if not self.sessions_file.exists():
            return {}
        
        try:
            with open(self.sessions_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.warning("Sessions file corrupted, starting fresh")
            return {}
