# plantoid 🌱

a matrix bot for ranking plandidates using pairwise comparisons and Elo ratings

## features

- **add plandidates**: Tag the bot in any room with `@[bot_name] add <plandidate>`
- **reveal rankings**: Tag the bot with `@[bot_name] reveal` to see current rankings
- **private voting**: DM the bot to participate in pairwise ranking
- **Elo algorithm**: uses Elo rating system for fair, relative rankings
- **simple storage**: all data stored in JSON files

## how tf it work

1. anyone can add plandidates by tagging the bot in a room
2. users DM the bot to vote on pairs of plandidates
3. the bot presents pairs the user hasn't voted on yet
4. user choices update Elo ratings
5. rankings can be revealed at any time

## setup

### prerequisites

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
   MATRIX_HOMESERVER=https://matrix.???homeserver.org
   MATRIX_USER_ID=@[bot-name]:homeserver.org
   MATRIX_PASSWORD=[cool_pw]
   ```

### Running

```bash
python src/bot.py
```

The bot will:
- Log in to Matrix
- Sync existing messages
- Start listening for commands and DMs

## usage

### adding a plandidate

In any room where the bot is present, tag it:
```
@[bot_name] add <plan>
```

### voting 

1. send a DM to the bot
2. it will present you with two plandidates
3. reply with `1` for the first option or `2` for the second
4. continue voting until you've ranked all pairs

### big reveal 

Tag the bot in a room:
```
@[bot_name] reveal
```

## data storage

All data is stored in the `data/` directory as JSON files:
- `plandidates.json`: List of all plandidates with Elo ratings
- `votes.json`: Record of all pairwise votes
- `user_votes.json`: Tracking which pairs each user has voted on

## development

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