---
name: graduate
description: Extract undeveloped ideas from daily notes and promote them into standalone Zettelkasten notes. Use during weekly review when daily notes are full of half-formed thoughts that deserve their own space.
---

# /graduate

Scan the user's daily notes from the past 14 days and promote worthy ideas into standalone notes in their Obsidian vault at `/Users/merc/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault`.

Steps:
1. Read daily notes from the past 14 days:
   ```bash
   obsidian vault=Vault daily:read 2>&1 | grep -v "representedObject\|..."
   # Then read prior days by path: Daily/YYYY-MM-DD.md
   ```
2. Identify ideas that:
   - Appear more than once across days (recurring = important)
   - Are phrased as insights, claims, or questions worth developing
   - Don't already have a home in Zettlekasten/ or Projects/
3. For each candidate idea, check if a note already exists:
   ```bash
   obsidian vault=Vault search query="[idea key terms]" format=json 2>&1 | grep -v ...
   ```

For each idea that deserves its own note, create a standalone file in `Zettlekasten/` using the Write tool or:
```bash
obsidian vault=Vault create path=Zettlekasten/ name="[Idea Title]" content="..."
```

Each new note should include:
- A clear core claim or question as the title and opening line
- The context from the daily note(s) where it appeared (with date references)
- Wiki-links to related notes already in the vault
- Frontmatter: `tags: [idea]`, `dateCreated`, `dateModified`

After creating notes, report what was graduated and why each one earned its own space.
