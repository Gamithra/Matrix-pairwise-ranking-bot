# Matrix pairwise ranking bot

A Matrix bot that enables collaborative ranking of items through pairwise comparisons using the Elo rating algorithm. Users compare items two at a time, and the bot maintains a dynamic ranking based on collective preferences.

## Features

- **Pairwise comparisons**: Present users with pairs of items to compare, making ranking intuitive and manageable
- **Elo rating system**: Uses the proven Elo algorithm (K-factor: 32) for fair and adaptive rankings
- **Direct message voting**: Private voting sessions through DMs with the bot
- **Public rankings**: Display current standings in Matrix rooms
- **Customizable terminology**: Configure the bot's language and personality to match your use case
- **Security**: Optional whitelist of authorized users
- **Persistent storage**: JSON-based storage with atomic writes to prevent data corruption
- **Progress tracking**: Shows users how many comparisons remain

## Use cases

- **Product prioritization**: Rank features, bugs, or product ideas
- **Team decision making**: Collaboratively rank proposals or options
- **Content curation**: Rank articles, resources, or content to surface the best
- **Event planning**: Rank venues, dates, or activity options
- **Anything else**: Adapt to your ranking needs with custom terminology

## Quick start

### Prerequisites

- Python 3.11+
- A Matrix account for the bot
- Access to a Matrix homeserver

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Gamithra/Matrix-pairwise-ranking-bot.git
   cd Matrix-pairwise-ranking-bot
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the bot**
   ```bash
   cp .env.example .env
   cp terminology.example.json terminology.json
   ```

   Edit `.env` with your Matrix credentials:
   - `MATRIX_HOMESERVER`: Your homeserver URL
   - `MATRIX_USER_ID`: Bot's Matrix user ID
   - `MATRIX_ACCESS_TOKEN` or `MATRIX_PASSWORD`: Authentication
   - `ALLOWED_USERS`: (Optional) Comma-separated user IDs

5. **Customize terminology** (optional)

   Edit `terminology.json` to customize the bot's language and personality. See [Customization](#customization) below.

6. **Run the bot**
   ```bash
   ./run.sh
   ```

## Usage

### Room commands

Mention the bot in any Matrix room to use these commands:

- **Add an item**: `@botname add <item name>`
- **Show rankings**: `@botname reveal`
- **Reset rankings**: `@botname rerank` (keeps items, clears votes)
- **Reset everything**: `@botname reset all` (deletes all data)
- **Help**: `@botname` (with no command)

### Voting via direct messages

1. Send a direct message to the bot
2. The bot will present you with pairs of items
3. Reply with `1` or `2` to indicate your preference
4. Continue until you've compared all possible pairs

The bot tracks your progress and only shows you pairs you haven't voted on yet.

## Customization

The bot's terminology and personality can be fully customized via `terminology.json`. This allows you to adapt the bot for different contexts without changing code.

### Example configuration

```json
{
  "item_name": "proposal",
  "item_name_plural": "proposals",
  "item_name_capitalized": "Proposal",
  "messages": {
    "add_success": "Added '{item}' to the ranking list.",
    "add_duplicate": "'{item}' is already in the list.",
    "reveal_header": "📊 **Current rankings** 📊",
    "reveal_empty": "No proposals to rank yet. Add some with `@{bot_name} add <proposal>`",
    "vote_intro": "Which proposal do you prefer?",
    "vote_option_format": "**{number}.** {item}",
    "vote_complete": "All comparisons complete! Rankings are now up to date.",
    "help_text": "Available commands:\n\n**In rooms:**\n- `@{bot_name} add <item>` - Add a new proposal\n- `@{bot_name} reveal` - Display current rankings\n\n**In direct messages:**\n- Message me to start pairwise ranking"
  }
}
```

### Customization fields

- **item_name**: Singular term for items being ranked
- **item_name_plural**: Plural term
- **item_name_capitalized**: Capitalized singular (for sentence starts)
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

### Key components

- **Terminology system**: Loads custom language from `terminology.json`
- **JSON storage**: Atomic writes prevent corruption
- **Elo ranking**: Implements chess-style rating updates
- **Pair selector**: Smart pairing ensures all combinations are covered
- **Event deduplication**: Prevents processing the same event twice
- **Session management**: Tracks user voting progress

## Development

### Running tests

```bash
# Run the example Elo demonstration
python3 src/example.py
```

### Project structure

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

## How Elo works

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

- **User whitelist**: Restrict bot usage to specific Matrix users via `ALLOWED_USERS` in `.env`
- **Access token auth**: Prefer access tokens over passwords in production
- **Event deduplication**: Prevents replay attacks and duplicate processing
- **Input validation**: All user inputs are validated before processing

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
