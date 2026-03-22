---
name: ghost
description: Answer a question the way the user would, based on their writing and stated beliefs. Use when you want to externalize your own thinking or need a draft response that sounds like you.
---

# /ghost

The user wants to know how they would answer a question, based on their own writing and beliefs in their Obsidian vault at `/Users/merc/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault`.

If the user provided a question, use it. Otherwise ask: "What question do you want answered in your voice?"

Then:
1. Search the vault for notes relevant to the question:
   ```bash
   obsidian vault=Vault search:context query="[key terms from question]" format=json 2>&1 | grep -v "representedObject\|Loading updated\|out of date\|installer\|Loaded main\|Ignored\|Checking\|Success\|Latest version\|App is up\|Obsidian\["
   ```
2. Read the most relevant notes — especially from Zettlekasten/, daily notes, and any notes where the user reflects or states opinions
3. Note the user's voice: how they phrase things, what they value, what they push back on
4. Look for direct quotes or strong statements that bear on the question

Output a response to the question written in the user's voice:
- Ground every claim in specific notes (cite them with [[Note Name]])
- Match their tone and framing
- Flag any tension or nuance in their notes — places where they've thought differently at different times
- Keep it honest: if the vault doesn't have a clear answer, say so and show what it does suggest
