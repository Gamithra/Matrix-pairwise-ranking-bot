# Planter 🌱

A Matrix bot for ranking "plandidates" (plan candidates) using pairwise comparisons and Elo ratings.

## Features

- **Add plandidates**: Tag the bot in any room with `@planter add <your plandidate>`
- **Reveal rankings**: Tag the bot with `@planter reveal` to see current rankings
- **Private voting**: DM the bot to participate in pairwise ranking
- **Elo algorithm**: Uses Elo rating system for fair, relative rankings
- **Simple storage**: All data stored in JSON files (no database needed!)

## How It Works

1. Anyone can add plandidates by tagging the bot in a room
2. Users DM the bot to vote on pairs of plandidates
3. The bot presents pairs the user hasn't voted on yet
4. User choices update Elo ratings
5. Rankings can be revealed at any time

## Setup

### Prerequisites

- Python 3.8+
- A Matrix account for the bot
- Access to a Matrix homeserver

### Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and configure:
   ```bash
   cp .env.example .env
   ```

4. Edit `.env` with your Matrix credentials:
   ```
   MATRIX_HOMESERVER=https://matrix.your-homeserver.org
   MATRIX_USER_ID=@planter:your-homeserver.org
   MATRIX_PASSWORD=your_secure_password
   ```

### Running

```bash
python src/bot.py
```

The bot will:
- Log in to Matrix
- Sync existing messages
- Start listening for commands and DMs

## Usage

### Adding a Plandidate

In any room where the bot is present, tag it:
```
@planter add Implement user authentication
```

### Voting on Pairs

1. Send a DM to the bot
2. It will present you with two plandidates
3. Reply with `1` for the first option or `2` for the second
4. Continue voting until you've ranked all pairs

### Revealing Rankings

Tag the bot in a room:
```
@planter reveal
```

## Data Storage

All data is stored in the `data/` directory as JSON files:
- `plandidates.json`: List of all plandidates with Elo ratings
- `votes.json`: Record of all pairwise votes
- `user_votes.json`: Tracking which pairs each user has voted on

## Development

The project structure:
```
planter/
├── src/
│   ├── bot.py              # Main bot entry point
│   ├── config.py           # Configuration
│   ├── storage/
│   │   ├── json_store.py   # JSON file operations
│   │   └── models.py       # Data models
│   ├── ranking/
│   │   ├── elo.py          # Elo algorithm
│   │   └── pairing.py      # Pair selection logic
│   ├── commands/
│   │   ├── add.py          # Add plandidate command
│   │   └── reveal.py       # Reveal rankings command
│   └── handlers/
│       ├── message.py      # Message handlers
│       └── dm.py           # DM voting handlers
└── data/                   # JSON data files
```

## License

MIT
# plantoid
