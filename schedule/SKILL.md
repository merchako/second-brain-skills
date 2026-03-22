---
name: schedule
description: Read priorities and tasks from the vault, then suggest how to allocate time this week. Use for weekly planning or when you need to map stated priorities to actual time blocks.
---

# /schedule

Read the user's priorities and tasks from their Obsidian vault at `/Users/merc/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault` and suggest a schedule for the week.

Steps:
1. Read today's and this week's daily notes for stated priorities and intentions:
   ```bash
   obsidian vault=Vault daily:read 2>&1 | grep -v "representedObject\|Loading updated\|out of date\|installer\|Loaded main\|Ignored\|Checking\|Success\|Latest version\|App is up\|Obsidian\["
   ```
2. Get all open and in-progress tasks with due/scheduled dates:
   - Grep for `status: open` and `status: doing` in `TaskNotes/Tasks/`
   - Read frontmatter for `due`, `scheduled`, and `priority` fields
3. Identify hot and spicy tasks — these anchor the schedule
4. Check for any overdue tasks (due before today)
5. Look at Projects/ for active work that needs time this week

Output a suggested weekly schedule:
- **Must do this week** — overdue, hot priority, or scheduled for this week
- **Should do this week** — spicy priority or progressing active projects
- **Nice to do** — normal/bland priority, no hard deadline
- **Suggested time blocks** — rough allocation by day, grouped by project or context

Then flag any conflicts:
- Tasks the user says matter but hasn't scheduled time for
- Overcommitment (too much for one week)
- Stated priorities that don't appear anywhere in the task list yet

Be honest about tradeoffs. If something has to slip, say so.
