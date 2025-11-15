# matrix pairwise ranking bot

a matrix bot for ranking stuff through pairwise comparisons so people can determine things they collectively want. uses elo ratings (like chess)!

## how it works

```
[in a room]
alice: @rankbot add pizza
bot: added 'pizza' to the ranking list.

alice: @rankbot add tacos
bob: @rankbot add burgers

alice: @rankbot reveal
bot: 📊 current rankings 📊
     1. pizza (1500 elo, 0 votes)
     2. tacos (1500 elo, 0 votes)
     3. burgers (1500 elo, 0 votes)

[alice DMs the bot]
bot: which do you prefer?
     1. pizza
     2. tacos
alice: 1

bot: which do you prefer?
     1. pizza
     2. burgers
alice: 2

bot: which do you prefer?
     1. tacos
     2. burgers
alice: 2

bot: all comparisons complete! rankings are now up to date.

[back in the room]
alice: @rankbot reveal
bot: 📊 current rankings 📊
     1. burgers (1516 elo, 2 votes)
     2. pizza (1508 elo, 2 votes)
     3. tacos (1476 elo, 2 votes)
```

## setup

you need python 3.11+ and a matrix account for the bot

```bash
git clone https://github.com/Gamithra/Matrix-pairwise-ranking-bot.git
cd Matrix-pairwise-ranking-bot

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
cp terminology.example.json terminology.json
```

edit `.env` with your matrix credentials:
- `MATRIX_HOMESERVER` - your homeserver url
- `MATRIX_USER_ID` - bot's user id  
- `MATRIX_ACCESS_TOKEN` or `MATRIX_PASSWORD` - auth
- `ALLOWED_USERS` - (optional) comma-separated list of allowed users

then start it:
```bash
./run.sh
```

## commands

**in rooms** (mention the bot):
- `@botname add <item>` - add something to rank
- `@botname reveal` - show current rankings
- `@botname rerank` - reset votes but keep items
- `@botname reset all` - delete everything
- `@botname` - show help

**in DMs** (private message the bot):
- just message it (with anything) and it'll walk you through comparing items
- it remembers which pairs you've already voted on

## customization

want to rank "proposals", or, "plans", instead of generic "items"? just edit `terminology.json`:

```json
{
  "item_name": "proposal",
  "item_name_plural": "proposals",
  "item_name_capitalized": "Proposal",
  "messages": {
    "add_success": "added '{item}' to the list!",
    "reveal_header": "📊 proposal rankings 📊",
    "vote_intro": "which proposal is better?",
    ...
  }
}
```

you can customize every message the bot sends. check `terminology.example.json` for all available options

## how elo works

items start at 1500 rating. when two items are compared:
1. expected outcome is calculated based on rating difference
2. actual outcome updates both ratings
3. beating a higher-rated item gives you more points

so if everyone keeps voting pizza > burgers, pizza's rating goes up and burgers goes down. the math stabilizes over time to reflect true preferences 🧑‍🔬

## deployment

see [DEPLOY.md](DEPLOY.md) for running this in production (systemd service, dedicated user, etc).

## notes

- built with [matrix-nio](https://github.com/poljar/matrix-nio)
- json storage (easy)
- elo k-factor of 32 for responsive but stable ratings
- deduplicates events to prevent double-processing
- tracks user progress so you don't see the same pair twice

## license

do whatever you want
