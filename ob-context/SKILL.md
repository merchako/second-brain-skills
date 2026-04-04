---
name: ob-context
description: Load full life and work state from the Obsidian vault — active projects, priorities, recent reflections. Use at the start of any session where the agent needs to know everything relevant about the user.
source: "Obsidian + Claude Codebook"
source_url: "https://drive.google.com/file/d/1p3xo7IHl_Dp8j9qJU6tR2OWVJB9_BYFP/view"
source_local: "[[Attachments/Obsidian + Claude Codebook (doc).pdf]]"
source_video: "https://www.youtube.com/watch?v=6MBq1paspVU"
source_notes: "[[Notes/Adding Second Brain Skills to Claude Code]], [[Notes/How I Use Obsidian + Claude Code to Run My Life (YouTube Clip)]]"
---

# /ob-context

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
