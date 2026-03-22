---
name: today
description: Pull daily note, tasks, and priorities into a plan for today. Use for morning planning or when overwhelmed and needing clarity on what matters.
---

# /today

Read the user's Obsidian vault at `/Users/merc/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault` and generate a prioritized plan for today.

Steps:
1. Read today's daily note: `obsidian vault=Vault daily:read 2>&1 | grep -v "representedObject\|Loading updated\|out of date\|installer\|Loaded main\|Ignored\|Checking\|Success\|Latest version\|App is up\|Obsidian\["`
2. Read open and in-progress task notes from `TaskNotes/Tasks/` — filter by `status: open` or `status: doing`
3. Surface any priorities, intentions, or focus areas mentioned in daily notes from the past 7 days
4. Check for overdue tasks (due date before today, 2026-03-21 format)

Output a prioritized plan for today:
- Lead with hot/spicy priority tasks and anything overdue
- Group remaining tasks by project or theme
- Note any intentions or focus the user set for this week
- Flag anything that looks like it should happen today based on scheduled dates

Keep it actionable and scannable.
