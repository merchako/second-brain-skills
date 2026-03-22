---
name: challenge
description: Pressure-test current beliefs by finding contradictions or weak points in the user's thinking. Use before making a big decision or when you want to stress-test an idea.
---

# /challenge

The user wants to stress-test their thinking on a topic using their Obsidian vault at `/Users/merc/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault`.

If the user provided a topic, use it. Otherwise ask: "What belief or idea do you want challenged?"

Then:
1. Search for all notes related to the topic:
   ```bash
   obsidian vault=Vault search:context query="[topic]" format=json 2>&1 | grep -v "representedObject\|Loading updated\|out of date\|installer\|Loaded main\|Ignored\|Checking\|Success\|Latest version\|App is up\|Obsidian\["
   ```
2. Read the relevant notes carefully — look across time, not just recent notes
3. Find places where the user has said contradictory things about this topic
4. Identify unstated assumptions embedded in how they write about it
5. Look for notes that implicitly undercut their stated position

Output a rigorous challenge:
- Where are they contradicting themselves? (cite specific notes)
- What assumptions are they making that might be wrong?
- What evidence in their own notes cuts against their current position?
- What questions aren't they asking that they should be?

Be direct. The point is to find the weak spots, not to validate.
