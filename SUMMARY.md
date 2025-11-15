# Planter Bot - Project Summary

## What We Built

A complete Matrix bot for collaborative ranking of "plandidates" (plan candidates) using:
- **Pairwise comparisons**: Users vote on pairs of options
- **Elo rating system**: Fair, relative rankings based on head-to-head comparisons
- **JSON storage**: Simple file-based storage (no database required!)
- **Matrix integration**: Public commands + private DM voting

## Architecture

### Storage Layer (`src/storage/`)
- **models.py**: Data models for Plandidate, Vote, and UserVotingSession
- **json_store.py**: All persistence logic using JSON files
  - `data/plandidates.json`: All plandidates with Elo ratings
  - `data/votes.json`: Historical vote records
  - `data/user_votes.json`: Tracks which pairs each user has voted on
  - `data/sessions.json`: Active DM voting sessions

### Ranking Layer (`src/ranking/`)
- **elo.py**: Classic Elo rating algorithm (K-factor = 32)
  - Calculates expected win probabilities
  - Updates ratings after each comparison
- **pairing.py**: Smart pair selection
  - Finds unvoted pairs for each user
  - Prioritizes pairs with similar Elo (most informative)
  - Tracks completion progress

### Commands Layer (`src/commands/`)
- **add.py**: Add new plandidates via `@planter add <name>`
- **reveal.py**: Show rankings via `@planter reveal`

### Handlers Layer (`src/handlers/`)
- **message.py**: Routes messages to commands or DM handler
- **dm.py**: Manages pairwise voting flow in DMs
  - Presents pairs automatically
  - Records votes and updates Elo
  - Shows progress

### Bot Entry Point (`src/bot.py`)
- Matrix client initialization
- Login and sync loop
- Event callback routing
- Error handling and logging

## User Flows

### 1. Adding a Plandidate
```
User (in room): @planter add Implement user authentication
Bot: ✅ Added plandidate: Implement user authentication
```

### 2. Voting on Pairs (DM)
```
User: (sends any message to bot)
Bot: Which plandidate do you prefer?

     1. Implement user authentication
     2. Add mobile app support
     
     Reply with 1 or 2
     
     (5 pairs remaining)

User: 1
Bot: ✅ Recorded your preference for Implement user authentication!
     
     Which plandidate do you prefer?
     [next pair...]
```

### 3. Revealing Rankings
```
User (in room): @planter reveal
Bot: 📊 Current Rankings

     1. 🥇 Implement user authentication (Elo: 1623, 12 votes)
     2. 🥈 Add mobile app support (Elo: 1542, 10 votes)
     3. 🥉 Improve search (Elo: 1498, 8 votes)
     ...
```

## Key Features

✅ **No restrictions**: Anyone can add plandidates  
✅ **Fair ranking**: Elo algorithm balances all comparisons  
✅ **Smart pairing**: Shows similar-rated options first  
✅ **Progress tracking**: Users see how many pairs remain  
✅ **Persistent storage**: All data saved in simple JSON files  
✅ **Clean architecture**: Modular, testable, maintainable  

## Quick Start

1. **Setup**:
   ```bash
   ./setup.sh
   ```

2. **Configure** (edit `.env`):
   ```
   MATRIX_HOMESERVER=https://matrix.your-server.org
   MATRIX_USER_ID=@planter:your-server.org
   MATRIX_PASSWORD=your_password
   ```

3. **Run**:
   ```bash
   ./run.sh
   ```

## Testing

Run the example to see how Elo works:
```bash
python3 example.py
```

## Future Enhancements (Optional)

- **Remove plandidates**: Add command to remove options
- **Reset rankings**: Clear all votes and start over
- **Vote history**: Show user's voting history
- **Multiple ranking lists**: Support different topics/channels
- **Web dashboard**: Visualize rankings over time
- **Elo decay**: Reduce ratings of old/inactive plandidates
- **Weighted voting**: Give more weight to experienced voters
- **Export results**: CSV/JSON export of rankings

## Dependencies

- `matrix-nio`: Modern async Python Matrix client
- `python-dotenv`: Environment variable management

That's it! Simple, clean, and ready to deploy. 🌱
