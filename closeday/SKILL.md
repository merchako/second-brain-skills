---
name: closeday
description: Capture what happened today and what was learned. Counterpart to /today. Use at end of day to log progress, capture new ideas, and clear your head before tomorrow.
---

# /closeday

Help the user close out their day by reviewing progress and updating their Obsidian vault at `/Users/merc/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault`.

## Step 0: Determine the review window

Before doing anything else, find the last close timestamp to know which git changes to include.

**Find the most recent `*Closed:` timestamp** from any daily note in the vault:

```bash
grep -r "^\*Closed: " "/Users/merc/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault/Daily/" 2>/dev/null | sort -r | head -1
```

This outputs something like:
```
/path/to/Daily/2026-03-22.md:*Closed: 17:30*
```

The timestamp is short (HH:MM only) — reconstruct the full datetime for git by extracting the date from the filename and combining it with the time:
- Filename `2026-03-22.md` → date `2026-03-22`
- Time from line: `17:30`
- Combined `LAST_CLOSE`: `"2026-03-22 17:30"`

- If a `LAST_CLOSE` is found, use it as the `--since` argument for all git log commands below.
- If no timestamp is found (first ever close), fall back to `"$(date '+%Y-%m-%d') 00:00"` (today at midnight).

## Steps

1. Read today's daily note to see what was planned:
   ```bash
   obsidian vault=Vault daily:read 2>&1 | grep -v "representedObject\|Loading updated\|out of date\|installer\|Loaded main\|Ignored\|Checking\|Success\|Latest version\|App is up\|Obsidian\["
   ```
2. Read task notes for anything marked `status: doing` — check if progress was made.
3. **Review git changes since last close:**
   - Get files changed since `LAST_CLOSE`:
     ```bash
     git -C "/Users/merc/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault" \
       log --since="LAST_CLOSE" --name-only --format="" | sort -u
     ```
   - Get currently modified/untracked files:
     ```bash
     git -C "/Users/merc/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault" status --short
     ```
   - Cross-reference these file paths against the daily note content. Flag any files that were changed but not mentioned.
   - Skim flagged files for unfinished markers (`TODO`, `...`, incomplete bullets, abrupt endings). Read files that seem noteworthy.
   - Build a short list: which changed files are accounted for in the daily note, which are not, and which look potentially unfinished.
4. **Audit repo health across `~/Developer/`:**
   - Find all git repos: `find ~/Developer -maxdepth 2 -name ".git" -type d | sed 's|/.git||'`
   - For each repo, check:
     - **Uncommitted changes**: `git -C <repo> status --porcelain` — non-empty = dirty
     - **Unpushed commits**: `git -C <repo> log @{u}..HEAD --oneline 2>/dev/null` — non-empty = unpushed (skip if no upstream)
     - **Current branch**: `git -C <repo> branch --show-current` — flag if not `main` or `master`
   - For each repo that needs attention, offer to fix it:
     - Dirty repo → offer to commit (ask for a message or suggest one)
     - Unpushed commits → offer to push
     - Non-main branch → offer to switch to main and pull
   - **If the user declines** because they're mid-work, that's fine — but note the repo and reason in the daily note under a **WIP Repos** section so it surfaces tomorrow with `/today`
5. Ask the user (if not already provided): "What did you work on today? Any new ideas or things to carry over?" — and present the git review findings so they can confirm or add context.

## Composing and appending the summary

Get the current time, then append to today's daily note. The timestamp **must be the first line after `## Day Close`** — this is what future `/closeday` runs use to find the review window boundary:

```bash
CLOSE_TIME=$(date '+%H:%M')
obsidian vault=Vault daily:append content="\n\n## Day Close\n*Closed: $CLOSE_TIME*\n\n[summary here]"
```

The summary should include:
- **Progress** — what actually got done (check off completed steps if applicable)
- **New ideas** — anything that came up worth remembering
- **Carry over** — unfinished items that should surface tomorrow
- **Loose ends** — files touched since `LAST_CLOSE` that look unfinished or weren't mentioned; brief note on their state so nothing falls through the cracks
- **WIP Repos** (if any) — repos the user couldn't clean up because they're mid-work; one line per repo with branch and reason

Also update task note statuses where work was completed:
```bash
obsidian vault=Vault property:set name=status value=done path=TaskNotes/Tasks/[task].md
obsidian vault=Vault property:set name=dateModified value=[today ISO] path=TaskNotes/Tasks/[task].md
```

End with a clean list of what to pick up tomorrow.
