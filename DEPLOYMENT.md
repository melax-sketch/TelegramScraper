# Deployment Guide for TelegramScraper

## Quick Start (Docker - Recommended)

### Prerequisites
- Docker & Docker Compose installed
- `.env` file with `API_ID` and `API_HASH` configured

### 1. Build & Run with Docker Compose

```bash
# Build the Docker image
docker-compose build

# Run the application
docker-compose up -d

# View logs
docker-compose logs -f
```

### 2. Execute Commands Inside Container

```bash
# Interactive terminal
docker-compose exec telegram-scraper python main.py

# For direct operations
docker-compose exec telegram-scraper python add_to_channel.py
```

### 3. Stop & Cleanup

```bash
# Stop running container
docker-compose down

# Remove all data (sessions, output)
docker-compose down -v
```

---

## Deployment Scenarios

### Option A: Linux VPS/Server (Ubuntu 20.04+)

#### 1. SSH into your server
```bash
ssh user@your_server_ip
```

#### 2. Install dependencies
```bash
sudo apt update && sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER
newgrp docker
```

#### 3. Clone & Deploy
```bash
git clone https://github.com/AbirHasan2005/TelegramScraper.git
cd TelegramScraper

# Create .env file
nano .env
# Add: API_ID=your_id, API_HASH=your_hash, SESSION_PASSWORD=your_password

# Deploy
docker-compose up -d
```

#### 4. Verify deployment
```bash
docker-compose ps
docker-compose logs
```

---

### Option B: Cloud Deployment

#### AWS EC2
1. Launch Ubuntu 22.04 instance (t3.small or larger)
2. Follow Linux VPS steps above
3. Open security group port if needed (only for API mode)

#### DigitalOcean Droplet
1. Create Ubuntu 22.04 droplet ($5/month minimum)
2. SSH and follow Linux VPS steps
3. Create firewall rules if needed

#### Google Cloud / Azure
1. Create Compute Engine VM or VM instance
2. SSH connection from console
3. Follow Linux VPS installation steps

---

### Option C: Background Service (Systemd)

Create `/etc/systemd/system/telegram-scraper.service`:

```ini
[Unit]
Description=Telegram Scraper Service
After=network.target
Requires=docker.service

[Service]
Type=simple
User=docker
WorkingDirectory=/home/user/TelegramScraper
ExecStart=/usr/bin/docker-compose up
ExecStop=/usr/bin/docker-compose down
Restart=unless-stopped
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-scraper
sudo systemctl start telegram-scraper
```

---

## Environment Configuration

### `.env` file template:
```env
# Required: Get from https://my.telegram.org/apps
API_ID=12345678
API_HASH=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional
SESSION_PASSWORD=your_secure_password
LOG_LEVEL=INFO
SESSIONS_DIR=./sessions
CSV_OUTPUT_DIR=./output
LOG_DIR=./logs
```

---

## Volume Management

### Important Paths (persisted in deployment):
- `/app/sessions/` - Telegram session files (do NOT lose these!)
- `/app/output/` - Scraped CSV files
- `/app/logs/` - Application logs

### Backup sessions:
```bash
docker-compose exec telegram-scraper tar -czf sessions_backup.tar.gz sessions/
docker cp telegram-scraper:/app/sessions_backup.tar.gz ./
```

### Restore sessions:
```bash
docker cp ./sessions_backup.tar.gz telegram-scraper:/app/
docker-compose exec telegram-scraper tar -xzf sessions_backup.tar.gz
```

---

## Monitoring & Logs

### View real-time logs:
```bash
docker-compose logs -f telegram-scraper
```

### Check container status:
```bash
docker-compose ps
docker stats telegram-scraper
```

### Health check:
```bash
docker-compose exec telegram-scraper python -c "from src.config import Config; Config.validate(); print('✓ Healthy')"
```

---

## Troubleshooting

### Container won't start
```bash
docker-compose logs telegram-scraper
# Check if API_ID and API_HASH are set in .env
```

### Out of memory
- Increase in docker-compose.yml: `memory: 2G`

### Permission denied
```bash
sudo chown -R $(id -u):$(id -g) ./sessions ./output ./logs
```

### Session expired
- Re-login: `docker-compose exec telegram-scraper python main.py` → Option 01

---

## Performance Tuning

For large-scale scraping, modify `docker-compose.yml`:

```yaml
environment:
  - MEMBERS_BATCH_SIZE=500
  - REQUEST_DELAY=0.5
  - BROADCAST_DELAY_MIN=20
  - BROADCAST_DELAY_MAX=40
```

---

## Security Best Practices

1. **Never commit `.env`** - Add to `.gitignore`
2. **Use strong SESSION_PASSWORD** - At least 16 characters
3. **Restrict server access** - Use firewall rules
4. **Backup sessions regularly** - Use automated scripts
5. **Rotate API credentials** - Monthly if possible
6. **Run as non-root** - Docker does this by default

---

## Uninstall/Cleanup

```bash
# Stop and remove container
docker-compose down

# Remove image
docker rmi telegramsscraper:latest

# Clean up all Docker data
docker system prune -a
```

---

For more help, check logs or contact support.
