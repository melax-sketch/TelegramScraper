# TelegramScraper - Setup & Run Guide

## ✅ Project Setup Complete!

The TelegramScraper project has been fully implemented with all features from the README.

### 📁 Project Structure

```
TelegramScraper/
├── main.py                 # Entry point - interactive CLI
├── requirements.txt        # Python dependencies
├── .env.example           # Configuration template
├── .env                   # Your configuration (fill with credentials)
├── .gitignore            # Git ignore rules
├── README.md             # Original project documentation
│
└── src/                  # Source code modules
    ├── __init__.py
    ├── config.py                # Configuration management
    ├── logger.py                # Logging setup (rotating files)
    ├── session_manager.py       # Session encryption & storage
    ├── telegram_client.py       # Pyrogram client wrapper
    ├── member_manager.py        # CSV & checkpoint management
    ├── scraper.py              # Member scraping logic
    ├── adder.py                # Member adding logic
    ├── broadcaster.py          # Message broadcasting
    └── ui.py                   # Rich terminal UI
```

### 🚀 Quick Start

#### 1. Get Telegram API Credentials

1. Visit [https://my.telegram.org/apps](https://my.telegram.org/apps)
2. Log in with your Telegram phone number
3. Click "Create New Application"
4. Copy your **API_ID** and **API_HASH**

#### 2. Configure .env File

Edit `.env` in the project root:

```env
API_ID=your_api_id_number_here
API_HASH=your_api_hash_string_here
SESSION_PASSWORD=your_secure_password_here
```

#### 3. Run the Application

```bash
cd /workspaces/TelegramScraper
python main.py
```

Or with the venv:

```bash
/workspaces/TelegramScraper/.venv/bin/python main.py
```

### 📋 Features Implemented

✅ **Multi-Account Support** - Manage multiple Telegram accounts  
✅ **3 Login Methods** - Phone number, OTP, or QR code support  
✅ **2 Scraping Modes**:
   - Visible members from chat member list
   - Hidden members from message history

✅ **2 Adding Modes**:
   - Rush Adder (fast, removes from CSV)
   - Calm Adder (slow with delays, keeps CSV)

✅ **Message Broadcasting** - Send DMs to scraped members with delays  
✅ **Session Encryption** - Fernet (AES) encryption with SHA256 key derivation  
✅ **FloodWait Handling** - Automatic waits with account rotation support  
✅ **Checkpoint Resume** - Save/resume scraping progress  
✅ **Rich Terminal UI** - Progress bars, spinners, colored output  
✅ **Session Management** - List, test, delete sessions  
✅ **Structured Logging** - Rotating file logs in `./logs/`  
✅ **Atomic CSV Writes** - Safe writes with temp files to prevent corruption  

### 📂 Data Directories

Created automatically when app runs:

- **`./sessions/`** - Encrypted session storage
- **`./output/`** - CSV files with member data
- **`./logs/`** - Application logs (rotating, 10MB max)

### 🔐 Security Features

- **Encrypted Sessions** - All session strings encrypted with Fernet
- **Password-Based Key Derivation** - SHA256 with salt
- **No Sensitive Logging** - Session strings never logged to files
- **Atomic Writes** - CSV operations protected from crashes

### 📦 Dependencies Installed

```
pyrogram==1.4.16         # Telegram client library
TgCrypto==1.2.5          # Fast crypto for Pyrogram
python-dotenv==1.0.0     # .env file support
rich==13.7.0             # Beautiful terminal UI
cryptography==41.0.7     # Encryption library
requests==2.31.0         # HTTP library
```

### 🎮 Menu Options

When you run `python main.py` you'll see:

```
01  Login Telegram Account
02  Manage Sessions
03  Scrape Group Members
04  Add Members to Group
05  Broadcast Message
06  View Logs
07  Exit
```

### 💾 CSV Format

Members are saved as CSV with columns:

```
user_id,username,first_name,last_name,is_bot,status
123456789,john_doe,John,Doe,False,member
987654321,jane_smith,Jane,Smith,False,member
```

### 📝 Example Workflow

1. **Login**
   ```
   Select: 01
   Enter account name: my_account
   Enter phone: +1234567890
   Enter OTP when prompted
   ```

2. **Scrape Members**
   ```
   Select: 03
   Enter account: my_account
   Enter group ID: -1001234567890
   Select scraping mode (visible/hidden)
   ```

3. **Add Members**
   ```
   Select: 04
   Enter account: my_account
   Enter group ID: -1001234567890
   Select adding mode (rush/calm)
   Enter CSV file: members_-1001234567890
   ```

4. **Broadcast**
   ```
   Select: 05
   Enter account: my_account
   Enter CSV file: members_list
   Enter markdown file: message.md
   Confirm broadcast
   ```

### 🛠️ Development Notes

**async/await**: All Telegram operations use async for performance  
**Progress Bars**: Real-time updates during long operations  
**Error Handling**: Comprehensive error logging and user feedback  
**Modular Design**: Each feature is in its own module for easy maintenance  

### 📊 Log Files

Logs are stored in `./logs/TelegramScraper.log`:

- Rotating: 5 backups, 10MB each
- All operations logged
- No sensitive data (session strings excluded)

### ⚠️ Important Notes

- Always use valid Telegram API credentials
- Keep `.env` file secure (contains API_HASH)
- Session passwords should be strong and unique
- Large member scraping may take time (no rate limits built in)
- Respect Telegram's ToS (don't spam users)

### 🐛 Troubleshooting

**"API_ID and API_HASH must be set"**
→ Update your `.env` file with valid credentials

**"Session not found"**
→ You need to login first (Menu option 01)

**"FloodWait error"**
→ Telegram rate limiting - wait or switch accounts

**"Failed to add members"**
→ Check user IDs are valid or try Calm mode with delays

---

## 🎉 Ready to Use!

The project is fully set up and ready to run. Just add your Telegram API credentials to `.env` and start the app!

```bash
python main.py
```

Good luck! 🚀
