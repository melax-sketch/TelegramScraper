#!/bin/bash

# Quick Deploy Script - TelegramScraper
# This script sets up everything needed for deployment

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔════════════════════════════════════╗"
echo "║  TelegramScraper Quick Deploy      ║"
echo "╚════════════════════════════════════╝"
echo -e "${NC}"

# Step 1: Check Docker
echo -e "\n${BLUE}[1/5] Checking Docker installation...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker not found. Install from: https://docs.docker.com/get-docker/${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker is installed${NC}"

# Step 2: Check Docker Compose
echo -e "\n${BLUE}[2/5] Checking Docker Compose installation...${NC}"
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}✗ Docker Compose not found. Install from: https://docs.docker.com/compose/install/${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose is installed${NC}"

# Step 3: Check .env file
echo -e "\n${BLUE}[3/5] Checking .env configuration...${NC}"
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠ .env file not found. Creating template...${NC}"
    cat > .env << 'EOF'
# Get these from https://my.telegram.org/apps
API_ID=YOUR_API_ID
API_HASH=YOUR_API_HASH

# Optional settings
SESSION_PASSWORD=changeme
LOG_LEVEL=INFO
SESSIONS_DIR=./sessions
CSV_OUTPUT_DIR=./output
LOG_DIR=./logs
EOF
    echo -e "${YELLOW}⚠ Please edit .env and add your API_ID and API_HASH${NC}"
    echo -e "${YELLOW}⚠ Get them from: https://my.telegram.org/apps${NC}"
    exit 1
fi

if ! grep -q "API_ID=" .env || [ -z "$(grep API_ID .env | cut -d= -f2 | tr -d ' ')" ]; then
    echo -e "${RED}✗ API_ID not configured in .env${NC}"
    exit 1
fi

if ! grep -q "API_HASH=" .env || [ -z "$(grep API_HASH .env | cut -d= -f2 | tr -d ' ')" ]; then
    echo -e "${RED}✗ API_HASH not configured in .env${NC}"
    exit 1
fi

echo -e "${GREEN}✓ .env is configured${NC}"

# Step 4: Create directories
echo -e "\n${BLUE}[4/5] Setting up directories...${NC}"
mkdir -p sessions output logs
chmod 755 sessions output logs
echo -e "${GREEN}✓ Directories created${NC}"

# Step 5: Build and start
echo -e "\n${BLUE}[5/5] Building and starting application...${NC}"
echo "Building Docker image..."
docker-compose build --quiet

echo "Starting application..."
docker-compose up -d

# Wait for startup
sleep 3

# Verify
if docker-compose ps | grep -q "telegram-scraper.*Up"; then
    echo -e "${GREEN}✓ Application started successfully${NC}"
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  Deployment Complete!             ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════╝${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Check status: docker-compose ps"
    echo "  2. View logs: docker-compose logs -f"
    echo "  3. Access app: docker-compose exec telegram-scraper python main.py"
    echo ""
    echo "Useful commands:"
    echo "  ./deploy.sh start    - Start application"
    echo "  ./deploy.sh stop     - Stop application"
    echo "  ./deploy.sh logs     - View live logs"
    echo "  ./deploy.sh backup   - Backup sessions and data"
    echo ""
else
    echo -e "${RED}✗ Failed to start application${NC}"
    echo "Checking logs..."
    docker-compose logs
    exit 1
fi
