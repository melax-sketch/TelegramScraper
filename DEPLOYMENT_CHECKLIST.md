# Pre-Deployment Checklist

## Prerequisites ✓
- [ ] Docker installed and running
- [ ] Docker Compose installed
- [ ] `.env` file created with `API_ID` and `API_HASH`
- [ ] Telegram account logged in (session already saved)
- [ ] GitHub repository cloned (optional, for automation)

## Configuration ✓
- [ ] API_ID is correct (get from https://my.telegram.org/apps)
- [ ] API_HASH is correct (get from https://my.telegram.org/apps)
- [ ] SESSION_PASSWORD is strong (16+ characters)
- [ ] All required volumes exist: `sessions/`, `output/`, `logs/`
- [ ] `.env` is in `.gitignore` (never commit credentials)

## Security ✓
- [ ] Remove any hardcoded credentials from code
- [ ] Use environment variables for all secrets
- [ ] Set strong access permissions: `chmod 700 sessions/`
- [ ] Enable firewall rules if accessing from specific IPs
- [ ] Create backup of sessions before deployment
- [ ] Test with read-only first, then expand permissions

## Testing ✓
- [ ] Test locally: `docker-compose up`
- [ ] Verify container starts successfully: `docker-compose ps`
- [ ] Test basic operations in container: `docker-compose exec telegram-scraper python main.py`
- [ ] Check logs for errors: `docker-compose logs`
- [ ] Test session persistence across restarts
- [ ] Verify volume mounts are working

## Deployment ✓

### Option 1: Docker Compose (Quick)
```bash
# Run deployment script
./deploy.sh start

# Or manual
docker-compose build
docker-compose up -d
```

### Option 2: Linux Server
```bash
# SSH to server and follow DEPLOYMENT.md instructions
ssh user@server_ip
git clone https://github.com/AbirHasan2005/TelegramScraper.git
cd TelegramScraper
nano .env  # Add credentials
./deploy.sh start
```

### Option 3: Cloud Platform
- [ ] Create VPS instance (Ubuntu 22.04)
- [ ] Install Docker/Docker Compose
- [ ] Clone repository
- [ ] Configure `.env`
- [ ] Run deployment

## Post-Deployment ✓
- [ ] Verify container is running: `docker-compose ps`
- [ ] Check logs are being generated: `ls -la logs/`
- [ ] Test scraping: `docker-compose exec telegram-scraper python main.py`
- [ ] Test member addition: `docker-compose exec telegram-scraper python add_to_channel.py`
- [ ] Monitor resource usage: `docker stats`
- [ ] Set up monitoring/alerts (optional)

## Backup Strategy ✓
- [ ] Backup sessions weekly
- [ ] Backup output data
- [ ] Use script: `./deploy.sh backup`
- [ ] Store backups in secure location
- [ ] Test recreation process

## Monitoring ✓
- [ ] Set up log rotation (if persistent)
- [ ] Monitor container health: `docker-compose ps`
- [ ] Check disk space regularly: `df -h`
- [ ] Monitor memory: `docker stats`
- [ ] Set up alerts for crashes

## Maintenance Schedule ✓
- [ ] Weekly: Check logs and status
- [ ] Monthly: Update Docker image
- [ ] Monthly: Backup sessions and data
- [ ] Quarterly: Review and update dependencies

## Rollback Plan ✓
- [ ] Keep previous Docker image
- [ ] Maintain backup of sessions
- [ ] Document deployment versions
- [ ] Test rollback procedure
- [ ] Store rollback commands

## Common Issues & Solutions ✓

| Issue | Solution |
|-------|----------|
| `docker-compose: command not found` | Install Docker Compose |
| `.env` file not found | Create `.env` with `API_ID` and `API_HASH` |
| Permission denied on volumes | Run `chmod 755 sessions/ output/ logs/` |
| Container crashes on start | Check logs: `docker-compose logs` |
| OOM (Out of Memory) | Increase memory limit in docker-compose.yml |
| Session expired | Re-login: `docker-compose exec telegram-scraper python main.py` |

## Deployment Success Criteria ✓
- [x] Container is running and healthy
- [x] Logs show no critical errors
- [x] Sessions are persisted
- [x] Application responds to commands
- [x] Data files are being created in `/app/output/`
- [x] No permission issues
- [x] Firewall rules (if applicable) are in place

---

**Date Deployed:** _______________  
**Deployed By:** _______________  
**Notes:** ___________________________


## Emergency Contacts
- GitHub Issues: https://github.com/AbirHasan2005/TelegramScraper/issues
- Author: @AbirHasan2005
