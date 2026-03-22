---
name: context
description: Load full life and work state from the Obsidian vault — active projects, priorities, recent reflections. Use at the start of any session where the agent needs to know everything relevant about the user.
---

# /context

Read the Obsidian vault at `/Users/merc/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault` and summarize the user's current context. Include:

- Active projects (check `Projects/` and task notes with `status: open` or `status: doing` in `TaskNotes/Tasks/`)
- Recent reflections and themes from daily notes in the past 7 days (`Daily/`)
- Any priorities, goals, or focus areas mentioned in the last 7 days
- Hot and spicy priority tasks (priority: hot or spicy in frontmatter)

Use the obsidian CLI to read notes. Filter CLI noise:
```bash
obsidian vault=Vault <command> 2>&1 | grep -v "representedObject\|Loading updated\|out of date\|installer\|Loaded main\|Ignored\|Checking\|Success\|Latest version\|App is up\|Obsidian\["
```

Present a concise briefing — what's active, what matters most, and what the user has been thinking about. This is the starting context for the session.
