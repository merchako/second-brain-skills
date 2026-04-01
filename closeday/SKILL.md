---
name: closeday
description: Capture what happened today and what was learned. Counterpart to /today. Use at end of day to log progress, capture new ideas, and clear your head before tomorrow.
---

# /closeday

Help the user close out their day by reviewing progress and taking notes.

## Step 0: Load config

Check for config at `~/.config/closeday.json`:

```bash
cat ~/.config/closeday.json 2>/dev/null
```

**If the file doesn't exist**, run first-time setup — ask the user:

1. "What directory holds your repos?" (default: `~/Developer`)
2. "How do you want to capture your daily close?"
   - **obsidian** — writes to an Obsidian vault via the Obsidian CLI
   - **markdown** — writes plain dated `.md` files to a folder you choose
   - **none** — repo audit and summary shown in terminal only, nothing written to disk
3. If `obsidian`: ask for the vault's absolute path and the vault name (the short name used in CLI commands, e.g. `Vault`)
4. If `markdown`: ask where to save notes (default: `~/Documents/closeday`)

Then write the config:

```bash
# obsidian example
cat > ~/.config/closeday.json << 'EOF'
{
  "repos_dir": "~/Developer",
  "notes_app": "obsidian",
  "obsidian_vault_path": "/path/to/vault",
  "obsidian_vault_name": "Vault"
}
EOF

# markdown example
cat > ~/.config/closeday.json << 'EOF'
{
  "repos_dir": "~/Developer",
  "notes_app": "markdown",
  "notes_dir": "~/Documents/closeday"
}
EOF

# none example
cat > ~/.config/closeday.json << 'EOF'
{
  "repos_dir": "~/Developer",
  "notes_app": "none"
}
EOF
```

Then continue with the steps below using the loaded config values.

**Config fields:**
| Field | Required | Description |
|---|---|---|
| `repos_dir` | always | Root directory to scan for git repos |
| `notes_app` | always | `"obsidian"`, `"markdown"`, or `"none"` |
| `obsidian_vault_path` | if obsidian | Absolute path to the vault |
| `obsidian_vault_name` | if obsidian | Short vault name used in CLI commands |
| `notes_dir` | if markdown | Directory where dated `.md` files are written |

---

## Step 1: Determine the review window

Find the most recent `*Closed:` line from a previous close to know what's new since then:

- **obsidian**: `grep -r "^\*Closed: " "<obsidian_vault_path>/Daily/" 2>/dev/null | sort -r | head -1`
- **markdown**: `grep -r "^\*Closed: " "<notes_dir>/" 2>/dev/null | sort -r | head -1`
- **none**: skip — use today at midnight as fallback

The line looks like: `/path/to/2026-03-22.md:*Closed: 17:30*`

Reconstruct the full datetime (`LAST_CLOSE`) by combining the date from the filename with the time from the line (e.g. `"2026-03-22 17:30"`). If nothing is found, fall back to `"$(date '+%Y-%m-%d') 00:00"`.

---

## Step 2: Read today's plan *(skip if `notes_app` is `"none"`)*

- **obsidian**:
  ```bash
  obsidian vault=<obsidian_vault_name> daily:read 2>&1 | grep -v "representedObject\|Loading updated\|out of date\|installer\|Loaded main\|Ignored\|Checking\|Success\|Latest version\|App is up\|Obsidian\["
  ```
- **markdown**: read `<notes_dir>/$(date '+%Y-%m-%d').md` if it exists

---

## Step 3: Read in-progress tasks *(obsidian only)*

Read task notes from `<obsidian_vault_path>/TaskNotes/Tasks/` — filter by `status: doing` — note whether progress was made on any of them.

---

## Step 4: Review notes/vault git changes since last close *(skip if `notes_app` is `"none"`)*

- **obsidian**: review the vault repo
  ```bash
  git -C "<obsidian_vault_path>" log --since="LAST_CLOSE" --name-only --format="" | sort -u
  git -C "<obsidian_vault_path>" status --short
  ```
- **markdown**: if `<notes_dir>` is a git repo, do the same; otherwise skip this step

Cross-reference changed files against today's plan. Flag anything unmentioned or that looks unfinished (contains `TODO`, `...`, or has an abrupt ending). Build a short list: accounted for / unaccounted for / potentially unfinished.

---

## Step 5: Audit repo health across `repos_dir`

Find all git repos:
```bash
find <repos_dir> -maxdepth 2 -name ".git" -type d | sed 's|/.git||'
```

For each repo, check:
- **Uncommitted changes**: `git -C <repo> status --porcelain` — non-empty = dirty
- **Unpushed commits**: `git -C <repo> log @{u}..HEAD --oneline 2>/dev/null` — non-empty = unpushed (skip if no upstream)
- **Current branch**: `git -C <repo> branch --show-current` — flag if not `main` or `master`

For each issue, offer to fix it:
- Dirty → offer to commit (ask for a message or suggest one)
- Unpushed → offer to push
- Non-main branch → offer to switch to main and pull

**If the user declines** because they're mid-work: note that repo and reason in the day's summary under **WIP Repos** so it surfaces tomorrow.

---

## Step 6: Ask what happened

Ask the user (if not already provided): "What did you work on today? Any new ideas or things to carry over?" — and present the findings from the steps above so they can confirm or add context.

---

## Composing and saving the summary

Build the close summary:
- **Progress** — what actually got done
- **New ideas** — anything worth remembering
- **Carry over** — unfinished items to pick up tomorrow
- **Loose ends** — changed files that look unfinished or weren't mentioned *(obsidian/markdown only)*
- **WIP Repos** (if any) — repos that couldn't be cleaned up; one line per repo with branch and reason

Then save based on `notes_app`:

**obsidian:**
```bash
CLOSE_TIME=$(date '+%H:%M')
obsidian vault=<obsidian_vault_name> daily:append content="\n\n## Day Close\n*Closed: $CLOSE_TIME*\n\n[summary]"
```
Also update completed task note statuses:
```bash
obsidian vault=<obsidian_vault_name> property:set name=status value=done path=TaskNotes/Tasks/[task].md
obsidian vault=<obsidian_vault_name> property:set name=dateModified value=[today ISO] path=TaskNotes/Tasks/[task].md
```

**markdown:**
```bash
CLOSE_TIME=$(date '+%H:%M')
NOTES_FILE="<notes_dir>/$(date '+%Y-%m-%d').md"
mkdir -p "<notes_dir>"
cat >> "$NOTES_FILE" << EOF

## Day Close
*Closed: $CLOSE_TIME*

[summary]
EOF
```

**none:** Display the full summary in the terminal. Nothing is written to disk.

---

End with a clean list of what to pick up tomorrow.
