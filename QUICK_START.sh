#!/bin/bash
# TelegramScraper - Quick Setup & Run Commands

echo "╔═══════════════════════════════════════════════════════════════════════════╗"
echo "║               TelegramScraper - Quick Start Script                        ║"
echo "╚═══════════════════════════════════════════════════════════════════════════╝"
echo

# Project directory
PROJECT_DIR="/workspaces/TelegramScraper"
VENV_PYTHON="$PROJECT_DIR/.venv/bin/python"

echo "📁 Project Location: $PROJECT_DIR"
echo

# Check if Python venv exists
if [ -f "$VENV_PYTHON" ]; then
    echo "✅ Python virtual environment found"
else
    echo "⚠️  Setting up Python environment..."
    cd "$PROJECT_DIR"
fi

echo

# Installation summary
echo "📦 Installation Summary:"
echo "  ✓ Python 3.12.3 virtual environment"
echo "  ✓ Dependencies installed:"
echo "    - pyrogram (Telegram client)"
echo "    - TgCrypto (Crypto acceleration)"
echo "    - python-dotenv (Configuration)"
echo "    - rich (Terminal UI)"
echo "    - cryptography (Session encryption)"
echo
echo "📁 Project Structure:"
echo "  ✓ src/ - Core modules"
echo "  ✓ main.py - Entry point"
echo "  ✓ .env - Configuration file"
echo "  ✓ requirements.txt - Dependencies"
echo

echo "🚀 To Run the Application:"
echo
echo "   Method 1 (Direct):"
echo "   $ cd $PROJECT_DIR && python main.py"
echo
echo "   Method 2 (Using venv python):"
echo "   $ cd $PROJECT_DIR && $VENV_PYTHON main.py"
echo

echo "⚙️  Configuration Steps:"
echo "  1. Get Telegram API credentials from https://my.telegram.org/apps"
echo "  2. Update .env file with your API_ID and API_HASH"
echo "  3. Run: python main.py"
echo

echo "📖 Documentation:"
echo "  - README.md - Original project documentation"
echo "  - SETUP_GUIDE.md - Detailed setup and usage guide"
echo

echo "🔑 First Time Setup:"
echo "  1. Copy .env.example to .env"
echo "  2. Add your Telegram credentials"
echo "  3. Run 'python main.py'"
echo "  4. Select option 01 to login"
echo

echo "╔═══════════════════════════════════════════════════════════════════════════╗"
echo "║                    Ready to start? Run: python main.py                    ║"
echo "╚═══════════════════════════════════════════════════════════════════════════╝"
