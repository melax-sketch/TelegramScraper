#!/bin/bash

# TelegramScraper Deployment Script
# Usage: ./deploy.sh [start|stop|restart|logs]

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}ℹ ${1}${NC}"
}

log_success() {
    echo -e "${GREEN}✓ ${1}${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠ ${1}${NC}"
}

log_error() {
    echo -e "${RED}✗ ${1}${NC}"
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        echo "Install Docker: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed"
        echo "Install Docker Compose: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    log_success "Docker and Docker Compose are installed"
}

check_env() {
    if [ ! -f .env ]; then
        log_error ".env file not found"
        echo "Please create .env with:"
        echo "  API_ID=your_id"
        echo "  API_HASH=your_hash"
        exit 1
    fi
    
    if ! grep -q "API_ID=" .env || ! grep -q "API_HASH=" .env; then
        log_error ".env file missing API_ID or API_HASH"
        exit 1
    fi
    
    log_success ".env file is configured"
}

build() {
    log_info "Building Docker image..."
    docker-compose build
    log_success "Docker image built"
}

start() {
    log_info "Starting TelegramScraper..."
    docker-compose up -d
    log_success "TelegramScraper started"
    
    sleep 2
    log_info "Container status:"
    docker-compose ps
}

stop() {
    log_info "Stopping TelegramScraper..."
    docker-compose down
    log_success "TelegramScraper stopped"
}

restart() {
    stop
    sleep 1
    start
}

logs() {
    log_info "Displaying logs (Ctrl+C to exit)..."
    docker-compose logs -f telegram-scraper
}

status() {
    log_info "Container status:"
    docker-compose ps
    
    log_info "Recent logs:"
    docker-compose logs --tail=20 telegram-scraper
}

backup() {
    log_info "Backing up sessions and data..."
    BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).tar.gz"
    
    tar -czf "$BACKUP_FILE" sessions/ output/ 2>/dev/null || true
    log_success "Backup created: $BACKUP_FILE"
}

show_help() {
    echo "TelegramScraper Deployment Script"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  start       - Start the application"
    echo "  stop        - Stop the application"
    echo "  restart     - Restart the application"
    echo "  logs        - View live logs"
    echo "  status      - Show container status"
    echo "  build       - Rebuild Docker image"
    echo "  backup      - Backup sessions and data"
    echo "  help        - Show this help message"
    echo ""
}

# Main
main() {
    case "${1:-help}" in
        start)
            check_docker
            check_env
            start
            ;;
        stop)
            stop
            ;;
        restart)
            check_docker
            check_env
            restart
            ;;
        logs)
            logs
            ;;
        status)
            status
            ;;
        build)
            check_docker
            build
            ;;
        backup)
            backup
            ;;
        help)
            show_help
            ;;
        *)
            log_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
