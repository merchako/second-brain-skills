---
name: connect
description: Bridge two domains or topics using the vault's link graph. Finds unexpected connections between ideas. Use when stuck or when you suspect two things are related but can't see how.
---

# /connect

The user wants to find connections between two topics in their Obsidian vault at `/Users/merc/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault`.

If the user provided two topics, use them. Otherwise ask: "What two topics or domains do you want to connect?"

Then:
1. Search for notes referencing topic A:
   ```bash
   obsidian vault=Vault search query="[topic A]" format=json 2>&1 | grep -v "representedObject\|Loading updated\|out of date\|installer\|Loaded main\|Ignored\|Checking\|Success\|Latest version\|App is up\|Obsidian\["
   ```
2. Search for notes referencing topic B (same pattern)
3. Find backlinks for the most central notes in each topic
4. Read the notes that appear in both search results, or that link between the two clusters
5. Look for shared tags, linked people, or shared projects

Output:
- The notes that serve as bridges between the two topics
- Any surprising or non-obvious connections
- Patterns you see across both domains
- A synthesis: what does the connection suggest the user might explore or create?
