---
name: closeday
description: Capture what happened today and what was learned. Counterpart to /today. Use at end of day to log progress, capture new ideas, and clear your head before tomorrow.
---

# /closeday

Help the user close out their day by reviewing progress and updating their Obsidian vault at `/Users/merc/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault`.

Steps:
1. Read today's daily note to see what was planned: `obsidian vault=Vault daily:read 2>&1 | grep -v "representedObject\|Loading updated\|out of date\|installer\|Loaded main\|Ignored\|Checking\|Success\|Latest version\|App is up\|Obsidian\["`
2. Read task notes for anything marked `status: doing` — check if progress was made
3. Ask the user (if not already provided): "What did you work on today? Any new ideas or things to carry over?"

Then compose a closing summary and append it to today's daily note:
```bash
obsidian vault=Vault daily:append content="\n\n## Day Close\n[summary]"
```

The summary should include:
- **Progress** — what actually got done (check off completed steps if applicable)
- **New ideas** — anything that came up worth remembering
- **Carry over** — unfinished items that should surface tomorrow

Also update task note statuses where work was completed:
```bash
obsidian vault=Vault property:set name=status value=done path=TaskNotes/Tasks/[task].md
obsidian vault=Vault property:set name=dateModified value=[today ISO] path=TaskNotes/Tasks/[task].md
```

End with a clean list of what to pick up tomorrow.
