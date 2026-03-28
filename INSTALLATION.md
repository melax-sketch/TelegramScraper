# TelegramScraper - Installation & Setup Guide

## Quick Start

### 1. Prerequisites
- Python 3.8 or higher
- Git
- C compiler (for TgCrypto compilation)

### 2. Install Dependencies

All dependencies are in `requirements.txt`. Install them with:

```bash
pip install -r requirements.txt
```

**Important:** TgCrypto is mandatory for performance. If installation fails:
- **Windows**: Install [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- **Linux/Termux**: `sudo apt install build-essential`
- **macOS**: `xcode-select --install`

### 3. Get Telegram API Credentials

1. Go to https://my.telegram.org/apps
2. Log in with your Telegram phone number
3. Click "Create New Application"
4. Fill in the form and copy your **API_ID** and **API_HASH**

### 4. Configure Environment

Create `.env` file in the project root:

```env
API_ID=your_api_id_here
API_HASH=your_api_hash_here
SESSION_PASSWORD=your_secure_password
LOG_LEVEL=INFO
```

Replace with your actual credentials.

### 5. Run the Application

```bash
python main.py
```

You should see the main menu with options to:
- Login Telegram Account
- Manage Sessions
- Scrape Group Members
- Add Members to Group
- Broadcast Message
- View Logs

## Project Structure

```
TelegramScraper/
├── main.py                 # Entry point
├── src/
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   ├── logger.py           # Logging setup
│   ├── ui.py              # Terminal UI (Rich)
│   ├── session_manager.py  # Session encryption & storage
│   ├── telegram_client.py  # Pyrogram wrapper
│   ├── scraper.py         # Member scraping
│   ├── adder.py           # Member adding
│   ├── broadcaster.py     # Message broadcasting
│   └── member_manager.py  # CSV/checkpoint management
├── sessions/              # Encrypted session storage
├── output/                # CSV output files
├── logs/                  # Application logs
├── requirements.txt       # Python dependencies
└── .env                   # Configuration (create from .env.example)
```

## Features

✅ **Multi-Account Support** - Log in multiple Telegram accounts
✅ **Session Encryption** - Secure session storage with Fernet
✅ **2 Scraping Modes** - Visible members or hidden from message history
✅ **2 Adding Modes** - Rush (fast) or Calm (slow with delays)
✅ **Message Broadcasting** - Send DM to all scraped members
✅ **FloodWait Handling** - Automatic wait handling
✅ **Checkpoint Resume** - Resume interrupted scrapes
✅ **Rich Terminal UI** - Progress bars, tables, colors
✅ **Rotating Logs** - Structured logging with rotation

## Troubleshooting

### "ModuleNotFoundError: No module named 'pyrogram'"
```bash
pip install pyrogram
```

### "ModuleNotFoundError: No module named 'cryptography'"
```bash
pip install cryptography
```

### "TgCrypto not available"
Install build tools and reinstall:
```bash
pip install tgcrypto
```

### "API_ID and API_HASH not set"
Make sure `.env` file exists with valid credentials:
```bash
cp .env.example .env
# Edit .env with your credentials
```

## Development Notes

- All sessions are encrypted with Fernet (AES-128) using PBKDF2
- Sensitive data (session tokens) never logged
- CSV writes are atomic (temp file first, then rename)
- Account cooldown tracking is persistent
- FloodWait automatically detected and handled

## License

See README.md for more information.
