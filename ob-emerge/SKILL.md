---
name: ob-emerge
description: Identify clusters of related ideas in the vault that are coalescing into something bigger — a project, essay, or product. Use when scattered thoughts are starting to cluster and you want to see what's ready to become real.
source: "Obsidian + Claude Codebook"
source_url: "https://drive.google.com/file/d/1p3xo7IHl_Dp8j9qJU6tR2OWVJB9_BYFP/view"
source_local: "[[Attachments/Obsidian + Claude Codebook (doc).pdf]]"
source_video: "https://www.youtube.com/watch?v=6MBq1paspVU"
source_notes: "[[Notes/Adding Second Brain Skills to Claude Code]], [[Notes/How I Use Obsidian + Claude Code to Run My Life (YouTube Clip)]]"
---

# /ob-emerge

Scan the user's Obsidian vault at `/Users/merc/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault` for clusters of related ideas that could become a project, essay, or product.

Steps:
1. Get vault structure overview:
   ```bash
   obsidian vault=Vault vault 2>&1 | grep -v "representedObject\|Loading updated\|out of date\|installer\|Loaded main\|Ignored\|Checking\|Success\|Latest version\|App is up\|Obsidian\["
   ```
2. Find notes with high backlink counts — these are gravitational centers of idea clusters:
   ```bash
   obsidian vault=Vault properties path=Zettlekasten format=json 2>&1 | grep -v ...
   ```
3. Check for unresolved links — topics the user references but hasn't written yet (latent demand):
   ```bash
   obsidian vault=Vault unresolved format=json 2>&1 | grep -v ...
   ```
4. Read recent daily notes and Zettlekasten notes to find ideas that are being revisited and refined
5. Look at Projects/ for anything aspirational that now has supporting notes elsewhere in the vault

Output: what's emerging?
- Name each cluster (2–5 words)
- List the notes that form its core
- Describe what kind of thing it wants to become: project, essay, product, conversation, something else
- Note what's missing before it's ready — what would make it real?

Prioritize clusters with momentum: multiple recent notes, cross-folder connections, recurring appearances.
