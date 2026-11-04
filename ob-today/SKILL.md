---
name: ob-today
description: Pull daily note, tasks, and priorities into a plan for today. Use for morning planning or when overwhelmed and needing clarity on what matters.
source: "Obsidian + Claude Codebook"
source_url: "https://drive.google.com/file/d/1p3xo7IHl_Dp8j9qJU6tR2OWVJB9_BYFP/view"
source_local: "[[Attachments/Obsidian + Claude Codebook (doc).pdf]]"
source_video: "https://www.youtube.com/watch?v=6MBq1paspVU"
source_notes: "[[Notes/Adding Second Brain Skills to Claude Code]], [[Notes/How I Use Obsidian + Claude Code to Run My Life (YouTube Clip)]]"
---

# /ob-today

Get recent info from the user's Obsidian vault to generate a daily brief for today:
- prioritized plan
- 3 days of reminders and look-aheads
- inferred blind spots, opportunities, and missed connections

Obsidian vault = `/Users/merc/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault`
Task manager = Tasks plugin in Obsidian, with tasks stored in `TaskNotes/Tasks/`. Docs - 


Steps:
1. Read today's daily note: `obsidian vault=Vault daily:read 2>&1 | grep -v "representedObject\|Loading updated\|out of date\|installer\|Loaded main\|Ignored\|Checking\|Success\|Latest version\|App is up\|Obsidian\["`
2. Read open and in-progress task notes from `TaskNotes/Tasks/` — filter by `status: open` or `status: doing`
3. Surface any priorities, intentions, or focus areas mentioned in daily notes from the past 7 days
4. Check for overdue tasks (due date before today, 2026-03-21 format)
5. List in-progress projects from the Bases view: `obsidian vault=Vault base:query path="Bases/Project Hub.base" view="Active Projects" format=md` (open project hubs, `doing` then `waiting`, with priority and due). Each name is a folder `Projects/<Name>/`; read a hub only if it bears on today.

Output a prioritized plan for today:
- Lead with hot/spicy priority tasks and anything overdue
- Group remaining tasks by project or theme
- Add a short **Active projects** list from step 5: one line each, `doing` first, with due dates; flag a `waiting` project that has been waiting long or has a due date this week
- Note any intentions or focus the user set for this week
- Flag anything that looks like it should happen today based on scheduled dates

Keep it actionable and scannable.
