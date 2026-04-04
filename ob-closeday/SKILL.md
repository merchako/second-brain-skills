---
name: ob-closeday
description: Capture what happened today and what was learned. Counterpart to /today. Use at end of day to log progress, capture new ideas, and clear your head before tomorrow.
source: "Obsidian + Claude Codebook"
source_url: "https://drive.google.com/file/d/1p3xo7IHl_Dp8j9qJU6tR2OWVJB9_BYFP/view"
source_local: "[[Attachments/Obsidian + Claude Codebook (doc).pdf]]"
source_video: "https://www.youtube.com/watch?v=6MBq1paspVU"
source_notes: "[[Notes/Adding Second Brain Skills to Claude Code]], [[Notes/How I Use Obsidian + Claude Code to Run My Life (YouTube Clip)]]"
---

# /ob-closeday

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

Then compute the **period label** used in the summary heading:

```bash
LAST_DATE=$(echo "$LAST_CLOSE" | awk '{print $1}')   # e.g. 2026-03-28
TODAY=$(date '+%Y-%m-%d')

if [ "$LAST_DATE" != "$TODAY" ]; then
  # Multi-day gap — format as a date range
  # macOS date parsing:
  START_LABEL=$(python3 -c "from datetime import date; d=date.fromisoformat('$LAST_DATE'); print(d.strftime('%b %-d'))")
  END_LABEL=$(python3 -c "from datetime import date; d=date.today(); print(d.strftime('%b %-d'))")
  PERIOD_LABEL="$START_LABEL – $END_LABEL"
else
  PERIOD_LABEL=$(python3 -c "from datetime import date; d=date.today(); print(d.strftime('%b %-d'))")
fi
```

Use `PERIOD_LABEL` wherever the day close is titled (e.g. `## Day Close — Mar 28 – Apr 1` vs `## Day Close — Apr 1`). Also mention the multi-day gap to the user so they're aware the summary covers several days.

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

### Link enrichment (do this before writing)

For every item you include in the summary, check whether a link is available and add it:

- **Already in the daily note log**: if the log entry for that item contains a Jira URL, GitHub PR link, or Discord thread link, use it rather than leaving the reference as plain text.
- **Jira tickets**: for any `PT-NNNN` reference, construct the link: `https://paratextstudio.atlassian.net/browse/PT-NNNN`. If you need the title or want to confirm the ticket exists, fetch it:
  ```bash
  JIRA_INSECURE=true jira issue view PT-NNNN --plain 2>/dev/null | head -5
  ```
- **Obsidian notes**: for any vault note mentioned (task notes, project notes, reference notes, etc.), use a wikilink (`[[Note Title]]`) if the note exists. Cross-reference against the list of changed files from Step 4 — anything that appeared there definitely exists.

Don't add links to things not mentioned in the summary. The goal is simply that what *is* mentioned is properly linked.

---

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

# 1. Append the Day Close section (date range in heading if multi-day)
obsidian vault=<obsidian_vault_name> daily:append content="\n\n## Day Close — $PERIOD_LABEL\n*Closed: $CLOSE_TIME*\n\n[summary]"

# 2. Insert a log entry into the ## Log section of today's daily note.
#    Format matches the QuickAdd "Log" template: blank line, @HH:MM, then bullet(s).
DAILY_FILE="<obsidian_vault_path>/Daily/$(date '+%Y-%m-%d').md"
python3 - <<PYEOF
import re
path = "$DAILY_FILE"
content = open(path).read()
entry = "\n@$CLOSE_TIME\n- /closeday: $ONE_LINE_SUMMARY\n"
# Insert immediately after the '## Log' heading line
content = re.sub(r'(## Log\n)', r'\1' + entry, content, count=1)
open(path, 'w').write(content)
PYEOF
```

Before running the Python block, set `ONE_LINE_SUMMARY` to a single concise sentence (≤ 10 words) describing what was done during the close period.

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

## Day Close — $PERIOD_LABEL
*Closed: $CLOSE_TIME*

[summary]
EOF
```

**none:** Display the full summary in the terminal. Nothing is written to disk.

---

End with a clean list of what to pick up tomorrow.
