# Deployment guide

## Server deployment

### 1. Prerequisites

On your server, ensure you have:
- Python 3.8+, at least, possibly 3.11+

### 2. Initial setup

```bash
# Navigate to deployment directory
cd /srv/rankbot

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit with your credentials
vim .env
```

Set these values in `.env`:
```
MATRIX_HOMESERVER=https://matrix.your.homeserver
MATRIX_USER_ID=@bot_name:matrix.your.homeserver
MATRIX_ACCESS_TOKEN=your_access_token_here
ALLOWED_USERS=@user1:matrix.server.com,@user2:matrix.server.com (leave empty to allow anyone)
```

### 4. Running with systemd (Recommended)

Create a systemd service file:

```bash
sudo vim /etc/systemd/system/rankbot.service
```

(ideally, create a new service user for this bot)

Content:
```ini
[Unit]
Description=Matrix ranking bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/srv/rankbot
Environment="PATH=/srv/rankbot/venv/bin"
ExecStart=/srv/rankbot/venv/bin/python3 /srv/rankbot/src/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable rankbot
sudo systemctl start rankbot
```

Check status:
```bash
sudo systemctl status rankbot
```

View logs:
```bash
sudo journalctl -u rankbot -f
```

### 5. Running with tmux (alternative)

```bash
# Create a tmux session
tmux new -s rankbot

# Run the bot
cd /srv/rankbot
source venv/bin/activate
./run.sh

# Detach with Ctrl+B, then D
# Reattach with: tmux attach -t rankbot
```

### 6. Updating

```bash
# Stop the bot
sudo systemctl stop rankbot

# Pull latest changes
git pull

# Install any new dependencies
source venv/bin/activate
pip install -r requirements.txt

# Restart
sudo systemctl start rankbot
```

### 7. Backup data

Your voting data is stored in `src/data/`. To backup:

```bash
# Backup
tar -czf rankbot-backup-$(date +%Y%m%d).tar.gz src/data/

# Restore
tar -xzf rankbot-backup-YYYYMMDD.tar.gz
```

### 8. Notes

- Keep your `.env` file secure (it contains your access token)
- use `ALLOWED_USERS` to restrict who can use the bot
- the `src/data/` directory contains all voting data - don't commit it to git
- regularly backup `src/data/` if the votes are important

### 9. Troubleshooting

**Bot not responding:**
```bash
# Check if it's running
sudo systemctl status rankbot

# Check logs
sudo journalctl -u rankbot -n 50
```

**Import errors:**
```bash
# Ensure you're using the venv
source venv/bin/activate
pip install -r requirements.txt
```

**Permission issues:**
```bash
# Ensure correct ownership
sudo chown -R your_user:your_user /srv/rankbot
```

**Data corruption:**
If JSON files get corrupted, stop the bot and manually fix or delete the corrupted file in `src/data/`.
