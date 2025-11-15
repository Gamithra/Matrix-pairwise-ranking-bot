# Matrix Pairwise Ranking Bot# plantoid 🌱



A Matrix bot that enables collaborative ranking of items through pairwise comparisons using the Elo rating algorithm. Users compare items two at a time, and the bot maintains a dynamic ranking based on collective preferences.a matrix bot for ranking plandidates using pairwise comparisons and Elo ratings



## Features## features



- **Pairwise Comparisons**: Present users with pairs of items to compare, making ranking intuitive and manageable- **add plandidates**: Tag the bot in any room with `@[bot_name] add <plandidate>`

- **Elo Rating System**: Uses the proven Elo algorithm (K-factor: 32) for fair and adaptive rankings- **reveal rankings**: Tag the bot with `@[bot_name] reveal` to see current rankings

- **Direct Message Voting**: Private voting sessions through DMs with the bot- **private voting**: DM the bot to participate in pairwise ranking

- **Public Rankings**: Display current standings in Matrix rooms- **Elo algorithm**: uses Elo rating system for fair, relative rankings

- **Customizable Terminology**: Configure the bot's language and personality to match your use case- **simple storage**: all data stored in JSON files

- **Security**: Optional whitelist of authorized users

- **Persistent Storage**: JSON-based storage with atomic writes to prevent data corruption## how tf it work

- **Progress Tracking**: Shows users how many comparisons remain

1. anyone can add plandidates by tagging the bot in a room

## Use Cases2. users DM the bot to vote on pairs of plandidates

3. the bot presents pairs the user hasn't voted on yet

- **Product Prioritization**: Rank features, bugs, or product ideas4. user choices update Elo ratings

- **Team Decision Making**: Collaboratively rank proposals or options5. rankings can be revealed at any time

- **Content Curation**: Rank articles, resources, or content to surface the best

- **Event Planning**: Rank venues, dates, or activity options## setup

- **Anything Else**: Adapt to your ranking needs with custom terminology

### prerequisites

## Quick Start

- Python 3.8+

### Prerequisites- A Matrix account for the bot

- Access to a Matrix homeserver

- Python 3.11+

- A Matrix account for the bot### Installation

- Access to a Matrix homeserver

1. Clone this repository

### Installation2. Install dependencies:

   ```bash

1. **Clone the repository**   pip install -r requirements.txt

   ```bash   ```

   git clone https://github.com/Gamithra/Matrix-pairwise-ranking-bot.git

   cd Matrix-pairwise-ranking-bot3. Copy `.env.example` to `.env` and configure:

   ```   ```bash

   cp .env.example .env

2. **Create a virtual environment**   ```

   ```bash

   python3 -m venv venv4. Edit `.env` with your Matrix credentials:

   source venv/bin/activate  # On Windows: venv\Scripts\activate   ```

   ```   MATRIX_HOMESERVER=https://matrix.???homeserver.org

   MATRIX_USER_ID=@[bot-name]:homeserver.org

3. **Install dependencies**   MATRIX_PASSWORD=[cool_pw]

   ```bash   ```

   pip install -r requirements.txt

   ```### Running



4. **Configure the bot**```bash

   ```bashpython src/bot.py

   cp .env.example .env```

   cp terminology.example.json terminology.json

   ```The bot will:

   - Log in to Matrix

   Edit `.env` with your Matrix credentials:- Sync existing messages

   - `MATRIX_HOMESERVER`: Your homeserver URL- Start listening for commands and DMs

   - `MATRIX_USER_ID`: Bot's Matrix user ID

   - `MATRIX_ACCESS_TOKEN` or `MATRIX_PASSWORD`: Authentication## usage

   - `ALLOWED_USERS`: (Optional) Comma-separated user IDs

### adding a plandidate

5. **Customize terminology** (optional)

   In any room where the bot is present, tag it:

   Edit `terminology.json` to customize the bot's language and personality. See [Customization](#customization) below.```

@[bot_name] add <plan>

6. **Run the bot**```

   ```bash

   ./run.sh### voting 

   ```

1. send a DM to the bot

## Usage2. it will present you with two plandidates

3. reply with `1` for the first option or `2` for the second

### Room Commands4. continue voting until you've ranked all pairs



Mention the bot in any Matrix room to use these commands:### big reveal 



- **Add an item**: `@botname add <item name>`Tag the bot in a room:

- **Show rankings**: `@botname reveal````

- **Reset rankings**: `@botname rerank` (keeps items, clears votes)@[bot_name] reveal

- **Reset everything**: `@botname reset all` (deletes all data)```

- **Help**: `@botname` (with no command)

## data storage

### Voting via Direct Messages

All data is stored in the `data/` directory as JSON files:

1. Send a direct message to the bot- `plandidates.json`: List of all plandidates with Elo ratings

2. The bot will present you with pairs of items- `votes.json`: Record of all pairwise votes

3. Reply with `1` or `2` to indicate your preference- `user_votes.json`: Tracking which pairs each user has voted on

4. Continue until you've compared all possible pairs

## development

The bot tracks your progress and only shows you pairs you haven't voted on yet.

The project structure:

## Customization```

planter/

The bot's terminology and personality can be fully customized via `terminology.json`. This allows you to adapt the bot for different contexts without changing code.├── src/

│   ├── bot.py              # Main bot entry point

### Example Configuration│   ├── config.py           # Configuration

│   ├── storage/

```json│   │   ├── json_store.py   # JSON file operations

{│   │   └── models.py       # Data models

  "item_name": "proposal",│   ├── ranking/

  "item_name_plural": "proposals",│   │   ├── elo.py          # Elo algorithm

  "item_name_capitalized": "Proposal",│   │   └── pairing.py      # Pair selection logic

  "bot_name": "DecisionBot",│   ├── commands/

  "bot_personality": "professional",│   │   ├── add.py          # Add plandidate command

  "messages": {│   │   └── reveal.py       # Reveal rankings command

    "add_success": "Added '{item}' to the ranking list.",│   └── handlers/

    "add_duplicate": "'{item}' is already in the list.",│       ├── message.py      # Message handlers

    "reveal_header": "📊 **Current Rankings** 📊",│       └── dm.py           # DM voting handlers

    "reveal_empty": "No proposals to rank yet. Add some with `@{bot_name} add <proposal>`",└── data/                   # JSON data files

    "vote_intro": "Which proposal do you prefer?",```
    "vote_option_format": "**{number}.** {item}",
    "vote_complete": "All comparisons complete! Rankings are now up to date.",
    "help_text": "Available commands:\\n\\n**In rooms:**\\n- `@{bot_name} add <item>` - Add a new proposal\\n- `@{bot_name} reveal` - Display current rankings\\n\\n**In direct messages:**\\n- Message me to start pairwise ranking"
  }
}
```

### Customization Fields

- **item_name**: Singular term for items being ranked
- **item_name_plural**: Plural term
- **item_name_capitalized**: Capitalized singular (for sentence starts)
- **bot_name**: How the bot refers to itself
- **bot_personality**: Freeform field for notes (not currently used)
- **messages**: All user-facing messages (supports {placeholders})

## Architecture

```
src/
├── bot.py              # Main bot entry point
├── config.py           # Configuration & terminology loading
├── commands/           # Command handlers (add, reveal, reset)
├── handlers/           # Event handlers (messages, DMs)
├── storage/            # Data persistence layer
├── ranking/            # Elo algorithm & pairing logic
└── data/               # Runtime data storage (gitignored)
```

### Key Components

- **Terminology System**: Loads custom language from `terminology.json`
- **JSON Storage**: Atomic writes prevent corruption
- **Elo Ranking**: Implements chess-style rating updates
- **Pair Selector**: Smart pairing ensures all combinations are covered
- **Event Deduplication**: Prevents processing the same event twice
- **Session Management**: Tracks user voting progress

## Development

### Running Tests

```bash
# Run the example Elo demonstration
python3 src/example.py
```

### Project Structure

- Commands are parsed via regex in `commands/` directory
- All user-facing text goes through `Terminology.get()`
- Storage operations use atomic writes via temp files
- Matrix events are deduplicated by `event_id`

## Deployment

See [DEPLOY.md](DEPLOY.md) for production deployment instructions including:
- Systemd service setup
- Running as dedicated user
- Security best practices
- Backup procedures

## How Elo Works

The Elo rating system (invented for chess) assigns each item a numerical rating. When two items are compared:

1. The expected outcome is calculated based on rating difference
2. The actual outcome (which item won) is compared to the expectation
3. Ratings are adjusted proportionally

**Key properties:**
- Items start at 1500 rating
- Beating a higher-rated item gives more points
- Ratings converge over time to reflect true preferences
- K-factor of 32 balances responsiveness and stability

## Security

- **User Whitelist**: Restrict bot usage to specific Matrix users via `ALLOWED_USERS` in `.env`
- **Access Token Auth**: Prefer access tokens over passwords in production
- **Event Deduplication**: Prevents replay attacks and duplicate processing
- **Input Validation**: All user inputs are validated before processing

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with clear commit messages
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with [matrix-nio](https://github.com/poljar/matrix-nio)
- Elo algorithm inspired by chess rating systems
- Designed for collaborative decision-making

## Support

- **Issues**: Report bugs or request features via GitHub Issues
- **Matrix**: Join `#matrix-dev:matrix.org` for Matrix development questions
- **Documentation**: See [Matrix Client-Server API](https://spec.matrix.org/latest/client-server-api/)
