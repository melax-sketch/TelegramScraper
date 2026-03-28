# Management Bot Setup Guide

## Overview
The Management Bot allows you to control the TelegramScraper remotely via Telegram commands. You can scrape groups, add members, and manage sessions without needing terminal access.

---

## Step 1: Create a Telegram Bot

### 1.1 Contact @BotFather
1. Open Telegram and search for **@BotFather**
2. Click Start or send `/start`
3. Send `/newbot` command
4. Follow the prompts:
   - **Name**: Enter your bot name (e.g., "ScrapeMan Bot")
   - **Username**: Enter a unique username (e.g., "@scraper_manager_bot")
5. **Copy the API token** (you'll need it in .env)

**Example token:** `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`

---

## Step 2: Get Your User ID

### 2.1 Get Your Telegram User ID
1. Search for **@userinfobot** on Telegram
2. Click Start
3. It will show your User ID
4. **Copy this ID** (you'll need it as OWNER_ID in .env)

**Example ID:** `123456789`

---

## Step 3: Configure .env

### 3.1 Add Bot Credentials
Edit your `.env` file and add:

```env
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
OWNER_ID=123456789
```

Replace with your actual values from steps 1 and 2.

---

## Step 4: Run the Bot

### Option A: Docker (Recommended)
```bash
docker-compose up -d management-bot

# View logs
docker-compose logs -f management-bot
```

### Option B: Local Python
```bash
python bot.py
```

You should see: ✅ Management bot started

---

## Step 5: Test the Bot

Open Telegram and search for your bot username (e.g., @scraper_manager_bot).

Send `/start` - you should receive a welcome message.

If you get "❌ Unauthorized": 
- Make sure OWNER_ID in .env is correct
- Restart the bot

---

## Available Commands

### `/start`
Shows welcome message and confirms bot is working.

```
Usage: /start
```

### `/help`
Shows all available commands with examples.

```
Usage: /help
```

### `/status`
Shows current system status and configuration.

```
Usage: /status
```

### `/sessions`
Lists all saved Telegram sessions.

```
Usage: /sessions
```

### `/scrape`
Scrape visible members from a group.

```
Usage: /scrape <account_name> <group_id>

Examples:
/scrape mela1 @MyGroup
/scrape my_account -1001234567890
```

### `/scrape_hidden`
Scrape members from message history (slower but finds more members).

```
Usage: /scrape_hidden <account_name> <group_id> <limit>

Examples:
/scrape_hidden mela1 @MyGroup 10000
/scrape_hidden account2 -1001234567890 50000
```

### `/add`
Add members from a CSV file to a channel.

```
Usage: /add <account> <channel_id> <csv_filename>

Examples:
/add mela1 -1002926828033 members
/add my_account -1001234567890 scraped_members
```

---

## Example Workflow

### Scenario: Add members from one group to another

**Step 1:** Scrape members
```
/scrape mela1 @SourceGroup
```
Bot responds:
```
✅ Scraping complete!

Group: Source Group Name
Members: 150
File: scrape_Source_Group_Name.csv
```

**Step 2:** Add members to target channel
```
/add mela1 -1002926828033 scrape_Source_Group_Name
```
Bot responds:
```
✅ Adding complete!

Added: 120
Failed: 30
```

---

## Troubleshooting

### Bot isn't responding
1. Check BOT_TOKEN is correct in .env
2. Restart bot: `docker-compose restart management-bot`
3. Check logs: `docker-compose logs management-bot`

### "❌ Unauthorized. Only owner can use this bot."
1. Verify your Telegram User ID is correct
2. Update OWNER_ID in .env
3. Restart the bot

### Bot can't find sessions
1. Make sure sessions are saved in the main scraper
2. Check `./sessions/` directory exists
3. Verify volume mounts in docker-compose.yml

### "❌ Error: API_ID and API_HASH must be set"
1. Add API_ID and API_HASH to .env
2. Get them from https://my.telegram.org/apps
3. Restart bot

### Scraping takes too long
1. Message the bot to check progress in logs
2. Monitor with: `docker-compose logs -f management-bot`
3. Large groups may take 10-30 minutes

---

## Security Best Practices

1. **Keep OWNER_ID secret** - Only you should know your Telegram ID
2. **Never share BOT_TOKEN** - It grants full bot control
3. **Use strong SESSION_PASSWORD** - 16+ characters
4. **Never commit .env** - Keep it in .gitignore
5. **Limit bot permissions** - Don't give admin rights unless needed
6. **Rotate BOT_TOKEN monthly** - Use BotFather to create new token
7. **Monitor bot logs** - Check for suspicious activity regularly

---

## Advanced Configuration

### Run Only the Bot (no scraper)
```bash
docker-compose up -d management-bot

# Or
python bot.py
```

### Run Both Services
```bash
docker-compose up -d

# Both telegram-scraper and management-bot start
```

### Stop Only the Bot
```bash
docker-compose stop management-bot
```

### View Real-time Bot Logs
```bash
docker-compose logs -f management-bot

# Or for all services
docker-compose logs -f
```

---

## Multiple Bots (Advanced)

You can create multiple bots for different purposes:

1. Create additional bots with @BotFather
2. Add multiple BOT_TOKEN entries to .env (modify docker-compose)
3. Create separate services in docker-compose.yml

---

## API Reference

### Bot Message Format

**Success:**
```
✅ Operation successful
Description: ...
```

**Error:**
```
❌ Error: description
```

**Status:**
```
⏳ Operation in progress...
```

---

## Support

For issues or feature requests:
- Check logs: `docker-compose logs management-bot`
- Review documentation: See DEPLOYMENT.md
- Check GitHub issues: https://github.com/AbirHasan2005/TelegramScraper/issues

---

## Quick Commands Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `/start` | Start bot | `/start` |
| `/help` | Show commands | `/help` |
| `/status` | System status | `/status` |
| `/sessions` | List accounts | `/sessions` |
| `/scrape` | Scrape members | `/scrape mela1 @group` |
| `/add` | Add members | `/add account -123 members.csv` |

---

## Next Steps

1. ✅ Create your bot with @BotFather
2. ✅ Get your User ID from @userinfobot
3. ✅ Add BOT_TOKEN and OWNER_ID to .env
4. ✅ Run: `docker-compose up -d management-bot`
5. ✅ Test: Message your bot with `/start`
6. ✅ Use commands to control scraper remotely

**Enjoy your management bot! 🤖**
