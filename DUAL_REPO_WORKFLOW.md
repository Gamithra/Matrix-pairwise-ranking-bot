# Dual Repository Workflow

This project maintains two Git repositories:

1. **Private repo** (`plantoid`): Your customized version with specific terminology and branding
2. **Public repo** (`Matrix-pairwise-ranking-bot`): Generic version for public use

## Setup

The repository is configured with two remotes:

```bash
git remote -v
# origin  git@github.com:Gamithra/plantoid.git (fetch/push)
# private git@github.com:Gamithra/planter.git (fetch/push)
# public  git@github.com:Gamithra/Matrix-pairwise-ranking-bot.git (fetch/push)
```

## What's Different Between Repos?

### Private Repo Only
- `terminology.json` - Your custom language/personality
- `README.private.md` - Your casual documentation
- `.env` - Your production credentials

### Public Repo Only
- `terminology.example.json` - Generic example configuration
- `README.md` - Professional generic documentation

### Shared (Both Repos)
- All Python source code (`src/`)
- Core infrastructure (`requirements.txt`, `run.sh`, etc.)
- `.gitignore`, `.env.example`
- `DEPLOY.md`, documentation

## Workflow Patterns

### Making Code Changes (Push to Both)

When you make changes to core functionality that should go to both repos:

```bash
# Make your changes
git add src/
git commit -m "Fix: Improve Elo calculation"

# Push to BOTH remotes
git push private main
git push public main
```

### Making Custom Changes (Private Only)

When you update your custom terminology or private docs:

```bash
# Edit your custom files
vim terminology.json
vim README.private.md

# Commit and push to private only
git add terminology.json README.private.md
git commit -m "Update plandidate messaging"
git push private main
```

### Before Pushing to Public

**ALWAYS** review what will be pushed:

```bash
# See what files have changed
git status

# See the actual changes
git diff public/main

# If terminology.json is staged, unstage it:
git reset HEAD terminology.json
```

### Safe Push Script

Create `push-public.sh` for safer public pushes:

```bash
#!/bin/bash
# Ensure we don't accidentally push private files

echo "Files to be pushed to public:"
git diff --name-only public/main

if git diff --name-only public/main | grep -q "terminology.json"; then
    echo "❌ ERROR: terminology.json would be pushed!"
    echo "Run: git reset HEAD terminology.json"
    exit 1
fi

if git diff --name-only public/main | grep -q "README.private.md"; then
    echo "❌ ERROR: README.private.md would be pushed!"
    exit 1
fi

echo "✅ Looks safe. Push to public? (y/n)"
read -r response
if [ "$response" = "y" ]; then
    git push public main
    echo "✅ Pushed to public"
else
    echo "❌ Cancelled"
fi
```

Make it executable:
```bash
chmod +x push-public.sh
```

## Gitignore Strategy

The `.gitignore` file is configured to exclude:

```gitignore
# Custom terminology (private repo only)
terminology.json

# Environment variables
.env
```

This means:
- ✅ `terminology.json` won't be tracked in public commits
- ✅ `.env` never goes to either repo
- ✅ `terminology.example.json` is tracked in both repos

## Pulling Updates

If you make changes on the public repo (e.g., accepting PRs):

```bash
# Pull from public
git pull public main

# Merge into private
git push private main
```

## Emergency: Accidentally Pushed Private Info

If you accidentally push private info to the public repo:

### Option 1: Revert the Commit (if just pushed)
```bash
git revert HEAD
git push public main
```

### Option 2: Force Push (if no one has pulled)
```bash
git reset --hard HEAD~1  # Go back one commit
git push public main --force
```

### Option 3: Remove from History (nuclear option)
```bash
# Use git filter-repo or BFG Repo-Cleaner
# Then force push
```

## Best Practices

1. **Always review before pushing to public**
   ```bash
   git diff public/main
   ```

2. **Keep terminology changes separate**
   - Commit code changes and terminology in separate commits
   - This makes it easier to push selectively

3. **Use descriptive commit messages**
   - Indicate if a commit is "[PUBLIC]" or "[PRIVATE]"
   - Example: `[PUBLIC] Fix: Handle empty item lists`
   - Example: `[PRIVATE] Update plandidate language`

4. **Test locally before pushing**
   - Run the bot with your changes
   - Verify nothing breaks

5. **Regular syncing**
   - Push to private frequently
   - Push to public only when features are complete

## Common Commands

```bash
# Status: Which remote are we ahead of?
git status
git log origin/main..HEAD        # Commits not in origin
git log private/main..HEAD       # Commits not in private
git log public/main..HEAD        # Commits not in public

# See differences between remotes
git diff public/main private/main

# Push to specific remote
git push private main
git push public main

# Pull from specific remote
git pull private main
git pull public main

# See all remotes
git remote -v
```

## Example Workflow Session

```bash
# 1. Make a bug fix
vim src/storage/json_store.py
git add src/storage/json_store.py
git commit -m "[PUBLIC] Fix: Prevent race condition in JSON writes"

# 2. Update your custom messaging
vim terminology.json
git add terminology.json
git commit -m "[PRIVATE] Update: More enthusiastic confirmation messages"

# 3. Push to both (only the public commit goes to public)
git push private main    # Pushes both commits
git push public main     # Pushes only the [PUBLIC] commit (terminology.json gitignored)

# 4. Later, update public README
vim README.md
git add README.md
git commit -m "[PUBLIC] Docs: Add troubleshooting section"
git push private main
git push public main
```

## Troubleshooting

**Q: I committed terminology.json but it's showing in `git status` for public push**

A: It shouldn't if `.gitignore` is correct. But if it does:
```bash
git rm --cached terminology.json
git commit -m "Remove terminology.json from tracking"
```

**Q: How do I know what's different between my repos?**

```bash
git diff public/main..private/main
```

**Q: Can I have different branches?**

Yes! You could use:
- `main` - stable releases
- `dev` - active development
- `private-main` - your customizations

Then merge `dev` → `main` → push to public when ready.

## Summary

- **Code changes**: Push to both repos
- **Custom changes**: Push to private only
- **Always review**: `git diff public/main` before pushing
- **Stay organized**: Use commit message prefixes
- **Keep .gitignore updated**: Ensure private files are excluded
