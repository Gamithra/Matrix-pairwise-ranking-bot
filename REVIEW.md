# 🔍 Pre-Push Review: Public Repo Changes

This document summarizes all changes that will be pushed to the public repository.

## Summary

We've genericized the codebase to support customizable terminology, allowing the public version to be used for any pairwise ranking use case while your private repo maintains the "plantoid/plandidate" branding.

## Files Modified for Public Release

### ✅ Safe to Push (Generic Changes)

#### 1. `src/config.py`
**Changes:**
- Added `Terminology` class that loads configuration from `terminology.json`
- Falls back to `terminology.example.json` if no custom file exists
- `Terminology.get()` method retrieves and formats messages

**Impact:** Enables full customization without code changes

#### 2. All Command Files (`src/commands/*.py`)
**Changes:**
- `add.py`: Uses `Terminology.get('messages.add_success')` instead of hardcoded "hell yeah, added..."
- `reveal.py`: Uses `Terminology.get('messages.reveal_header')` instead of "current rankings"
- `reset.py`: Uses `Terminology.get('messages.reset_all_confirm')` etc.

**Impact:** No more "plandidate" or "plantoid" references in code

#### 3. `src/handlers/dm.py`
**Changes:**
- Loads `item_name`, `item_name_plural` from terminology config
- All voting messages use `Terminology.get('messages.*')`
- Generic variable names (`items` instead of `plandidates`)

**Impact:** DM voting messages are now customizable

#### 4. `src/handlers/message.py`
**Changes:**
- Help message uses `Terminology.get('messages.help_text')`
- Imports `Terminology` from config

**Impact:** Help text is customizable

#### 5. `.gitignore`
**Changes:**
- Added `terminology.json` to gitignore (private only)
- Public repo will only have `terminology.example.json`

**Impact:** Your custom terminology won't leak to public repo

#### 6. `.env.example`
**Changes:**
- Updated default user from `@planter:example.org` to `@rankbot:example.org`
- Removed your specific user ID from ALLOWED_USERS example
- Changed display name to "RankBot"

**Impact:** Generic example configuration

#### 7. `README.md` (NEW - replaces old README)
**Changes:**
- Complete rewrite
- Professional tone
- No references to "plandidate" or "plantoid"
- Comprehensive setup instructions
- Customization documentation
- Architecture overview
- Use cases section

**Impact:** Public-facing documentation

### ✨ New Files (Public)

#### 1. `terminology.example.json`
**Contains:**
- Generic example configuration
- Professional language ("item", "proposal", etc.)
- Template for customization
- All message strings with placeholders

**Purpose:** Template for users to create their own `terminology.json`

#### 2. `DUAL_REPO_WORKFLOW.md`
**Contains:**
- Instructions for managing two repos
- Safe push workflows
- Gitignore strategy
- Troubleshooting

**Purpose:** Help you (and contributors) manage the dual-repo setup

#### 3. `README.private.md`
**Contains:**
- Your original casual README
- Plantoid-specific documentation

**Purpose:** Keep your private docs (won't be pushed to public)

### 🔒 Files That Stay Private

These files are configured to **NOT** be pushed to public:

1. **`terminology.json`** - Your custom plantoid language (gitignored)
2. **`README.private.md`** - Your casual docs (not added to public commits)
3. **`.env`** - Your credentials (already gitignored)
4. **`src/data/`** - Runtime data (already gitignored)

## What Will NOT Change

✅ All core functionality remains identical  
✅ Elo algorithm unchanged  
✅ Storage layer unchanged  
✅ Command parsing logic unchanged  
✅ Security features unchanged  

## Testing Recommendations

Before pushing to public, test locally:

```bash
# Test with generic terminology
cp terminology.example.json terminology.json
./run.sh

# In Matrix, test:
# 1. Add an item
# 2. Check rankings
# 3. Vote in DMs
# 4. Check help message

# Then restore your custom terminology
git checkout terminology.json
```

## Git Commands to Execute

### Review the changes:
```bash
git diff                    # See all changes
git status                  # See what files changed
```

### Stage for commit:
```bash
# Stage all modified files
git add src/
git add .gitignore
git add .env.example
git add README.md

# Stage new files (will go to both repos)
git add terminology.example.json
git add DUAL_REPO_WORKFLOW.md

# Keep your private README (don't add to git, or keep it separate)
git add README.private.md  # This can go to private repo only
```

### Commit and push:
```bash
# Commit the changes
git commit -m "Refactor: Add terminology system for customizable branding

- Add Terminology class for loading custom language
- Extract all hardcoded strings to terminology.json
- Add terminology.example.json template for public use
- Update README.md with generic documentation
- Add DUAL_REPO_WORKFLOW.md for repo management
- Update .gitignore to exclude terminology.json from public repo"

# Push to private first (test)
git push private main

# Review what would go to public
git diff public/main

# Push to public (after review)
git push public main
```

## Verification Checklist

Before pushing to public, verify:

- [ ] No "plandidate" strings in `src/` code (except variable names internally, which is fine)
- [ ] No "plantoid" references in public-facing strings
- [ ] `terminology.json` is in `.gitignore`
- [ ] `terminology.example.json` has generic language
- [ ] `README.md` is professional and generic
- [ ] `.env.example` has no personal info
- [ ] All code still works with `terminology.example.json`

## Expected Public Repository Structure

After push, the public repo will have:

```
Matrix-pairwise-ranking-bot/
├── src/                          # All source code (generic)
├── terminology.example.json      # Template configuration
├── .env.example                  # Environment template
├── README.md                     # Generic documentation
├── DUAL_REPO_WORKFLOW.md        # Repo management guide
├── DEPLOY.md                     # Deployment guide
├── requirements.txt              # Dependencies
├── run.sh                        # Run script
└── .gitignore                   # Excludes terminology.json
```

## Expected Private Repository Structure

Your private repo will have:

```
planter/
├── src/                          # All source code
├── terminology.json              # YOUR custom language (gitignored from public)
├── terminology.example.json      # Generic template
├── .env                          # YOUR credentials (gitignored)
├── .env.example                  # Template
├── README.md                     # Generic documentation
├── README.private.md             # YOUR casual docs
├── DUAL_REPO_WORKFLOW.md        # Repo management
├── DEPLOY.md                     # Deployment guide
└── ...
```

## Risk Assessment

**Low Risk:**
- ✅ All changes are additive (no functionality removed)
- ✅ Terminology system falls back to safe defaults
- ✅ Private files protected by gitignore
- ✅ No credentials or personal data in commits

**What Could Go Wrong:**
- ⚠️ If `terminology.json` is accidentally committed: Remove with `git rm --cached terminology.json`
- ⚠️ If you forget to test with generic terminology: Bot might not work for public users

## Questions to Consider

1. **Is the generic terminology.example.json appropriate?**
   - Current: Professional, formal language
   - Alternative: Could be more friendly/casual while still generic

2. **Is the README.md helpful for new users?**
   - Includes: Setup, usage, customization, architecture
   - Consider: Add more examples or screenshots?

3. **Are there any lingering plantoid references?**
   - Code: All genericized
   - Comments: Should be reviewed
   - Variable names: Some internal names like `plandidate_a` remain but not user-facing

## Next Steps

1. **Review this document** ✓ You're doing this now!
2. **Test with generic config** - Ensure it works
3. **Review diffs** - `git diff`
4. **Commit changes** - As shown above
5. **Push to private** - Test first
6. **Push to public** - After final approval

---

**Ready to proceed? Say the word and I'll commit and push these changes!**
