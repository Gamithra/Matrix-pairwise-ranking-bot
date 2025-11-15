# Deployment Guide

## Server Deployment

### 1. Prerequisites

On your server, ensure you have:
- Python 3.8+
- Git (if cloning from a repository)

### 2. Initial Setup

```bash
# Navigate to deployment directory
cd /srv/planter

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
nano .env
```

Set these values in `.env`:
```
MATRIX_HOMESERVER=https://matrix.campaignlab.uk
MATRIX_USER_ID=@operator:matrix.campaignlab.uk
MATRIX_ACCESS_TOKEN=your_access_token_here
ALLOWED_USERS=@user1:matrix.campaignlab.uk,@user2:matrix.campaignlab.uk
```

### 4. Running with systemd (Recommended)

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/planter.service
```

Content:
```ini
[Unit]
Description=Planter Matrix Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/srv/planter
Environment="PATH=/srv/planter/venv/bin"
ExecStart=/srv/planter/venv/bin/python3 /srv/planter/src/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable planter
sudo systemctl start planter
```

Check status:
```bash
sudo systemctl status planter
```

View logs:
```bash
sudo journalctl -u planter -f
```

### 5. Running with tmux (Alternative)

```bash
# Create a tmux session
tmux new -s planter

# Run the bot
cd /srv/planter
source venv/bin/activate
./run.sh

# Detach with Ctrl+B, then D
# Reattach with: tmux attach -t planter
```

### 6. Updating

```bash
# Stop the bot
sudo systemctl stop planter

# Pull latest changes
git pull

# Install any new dependencies
source venv/bin/activate
pip install -r requirements.txt

# Restart
sudo systemctl start planter
```

### 7. Backup Data

Your voting data is stored in `src/data/`. To backup:

```bash
# Backup
tar -czf planter-backup-$(date +%Y%m%d).tar.gz src/data/

# Restore
tar -xzf planter-backup-YYYYMMDD.tar.gz
```

### 8. Security Notes

- Keep your `.env` file secure (it contains your access token)
- Use `ALLOWED_USERS` to restrict who can use the bot
- The `src/data/` directory contains all voting data - don't commit it to git
- Regularly backup `src/data/` if the votes are important

### 9. Troubleshooting

**Bot not responding:**
```bash
# Check if it's running
sudo systemctl status planter

# Check logs
sudo journalctl -u planter -n 50
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
sudo chown -R your_user:your_user /srv/planter
```

**Data corruption:**
If JSON files get corrupted, stop the bot and manually fix or delete the corrupted file in `src/data/`.
