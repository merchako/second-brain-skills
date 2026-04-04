---
name: ob-tidy
description: Clean up messy notes in the Obsidian vault — fix errors, group related thoughts, add headings, promote fragments to task/Zettelkasten notes, and propose all changes via a git branch for review in VSCode.
source: "Obsidian + Claude Codebook"
source_url: "https://drive.google.com/file/d/1p3xo7IHl_Dp8j9qJU6tR2OWVJB9_BYFP/view"
source_local: "[[Attachments/Obsidian + Claude Codebook (doc).pdf]]"
source_video: "https://www.youtube.com/watch?v=6MBq1paspVU"
source_notes: "[[Notes/Adding Second Brain Skills to Claude Code]], [[Notes/How I Use Obsidian + Claude Code to Run My Life (YouTube Clip)]]"
---

# /ob-tidy

Clean up one or more messy notes in the Obsidian vault at `/Users/merc/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault`.

## When to use

Run `/tidy` on:
- A standalone note you've drafted verbosely or messily
- A daily note mid-day to add structure without closing the day
- A batch of `#inbox`-tagged notes (pass multiple paths or ask user to list them)

Do NOT run on notes that are already clean and structured unless the user asks.

---

## Arguments

- **File path or name**: path(s) to clean, e.g. `Daily/2026-03-26.md` or just a note name
- If no argument: get the active note from Obsidian CLI (`obsidian vault=Vault open:get-active 2>&1`)
- If still nothing: list `#inbox`-tagged notes and ask user which to process

---

## Step 0: Setup — create a cleanup branch

Before making any changes, create a dated cleanup branch so all changes are reviewable in VSCode before merging.

```bash
VAULT="/Users/merc/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault"
BRANCH="cleanup/$(date '+%Y-%m-%d')"

# If branch already exists today, append a counter
git -C "$VAULT" rev-parse --verify "$BRANCH" 2>/dev/null && \
  BRANCH="cleanup/$(date '+%Y-%m-%d')-2"

git -C "$VAULT" checkout -b "$BRANCH"
echo "Working on branch: $BRANCH"
```

---

## Step 1: Read and classify each note

For each note to process:

1. **Read the full content**
2. **Determine the note's primary type** (see classification rules below)
3. **Inventory all fragments** — list every distinct idea/item in the note and its proposed destination

### Note classification rules

| Signal | Classification |
|--------|---------------|
| Has `tags: [task]` or `status: do/doing/done` frontmatter | Task note — use task note template |
| Prefixed `To Do:`, `TODO`, `- [ ]` or tagged `#idea` (actionable) | Task fragment → promote to new task note |
| Tagged `#concept` or is an abstract principle/framework | Concept note → `Zettlekasten/Concepts/` |
| Looks like a meeting (attendees, agenda, action items) | Meeting note → promote if long/complex |
| Direct quote with attribution | Quote note → `Zettlekasten/Quotes/` |
| From a book/article/video/newsletter | Source note → `Zettlekasten/Sources/` |
| About a person | People note → `Zettlekasten/People/` |
| About a place | Places note → `Zettlekasten/Places/` |
| About an organization (school, church, company, group) | Org note → `Zettlekasten/Organizations/` |
| Tagged `#inbox` | Unprocessed — apply this full workflow |
| In `Inbox/` folder | Homeless draft — classify and move |

**Ambiguous ideas**: if a fragment has no `#idea`/`#concept` tag and you cannot determine whether it's actionable or conceptual, embed a question (see Step 3) rather than guessing.

**Places vs. Organizations**: classify by primary function. A school, church, or company is an Organization. A building, neighborhood, or city is a Place. If both apply, classify as Organization and add a `location` property linking to a Places note if one exists.

### Promotion thresholds

Promote a fragment OUT of the current note when ANY of the following are true:
- It would take more than ~5 minutes to act on (i.e., it's a real task, not a quick action)
- It is an `#idea` (actionable) — always promote to a task note
- It is a `#concept` — always promote to Zettlekasten/Concepts/
- It has 3+ sentences or multiple sub-points (too complex to live inline)
- It is meeting notes with more than a couple lines
- It is a direct quote
- It is a reading fragment from an external source

Keep in the note when:
- It is a brief reflection (1–2 sentences)
- It is a quick action already done (log entry)
- It is meeting notes that are just a line or two

---

## Step 2: Produce a cleaned version of each note

Apply these transformations:

### Structural cleanup
- Fix typos, grammar errors, incomplete sentences (use judgment — don't rewrite the user's voice)
- Group related bullets/fragments together (maintain rough chronological order within groups)
- Add `##` headings to separate distinct topics. Use `###` for sub-topics.
- Remove duplicate information
- Convert loose `To Do:` or `TODO` prefixes to `- [ ]` checkboxes if staying in the note, or flag for promotion

### Title inference
- If the note has a generic or missing title, infer a clean title from the dominant topic
- If uncertain, propose a title and mark it with `%% TIDY: Proposed title — confirm? %%`

### Frontmatter
Add or populate these properties if missing:
```yaml
---
date: YYYY-MM-DD          # date of the note or today
dateCreated: ISO8601
dateModified: ISO8601
tags:
  - [inferred tag(s)]
related:
  - "[[linked note]]"     # any notes mentioned in content or clearly related
status: [if applicable]
---
```

Use existing tags from content signals. Common tags: `daily`, `meeting`, `task`, `concept`, `idea`, `reading`, `reflection`, `inbox`.

Remove `#inbox` from tags once the note has been processed.

### For daily notes specifically
- Keep the `## Log` and `## Today's Notes` sections from the Daily Note Template
- Add topical sub-headings under `## Today's Notes` (e.g., `### Meetings`, `### Ideas`, `### Reflections`)
- Promote fragments per the thresholds above and replace with wikilinks: `[[Promoted Note Title]]`
- Do NOT add a close-of-day section (that belongs to `/closeday`)

---

## Step 3: Embed clarifying questions for uncertain items

When you are unsure about something — classification, title, whether to promote, who a person is, what a fragment means — embed an Obsidian comment directly in the note at the relevant location:

```
%% TIDY: [your question here] %%
```

Examples:
```
%% TIDY: Is "the design sprint idea" an actionable task or a concept to explore? (reply here) %%
%% TIDY: Who is "Mike" — is this [[Mike Cochran]]? (reply here) %%
%% TIDY: This fragment seems unfinished — what did you mean to capture here? (reply here) %%
```

Batch all questions — embed them all in one pass, then commit. Do not ask questions one by one in chat if there are more than 2–3.

If there are so many questions that it would make the note unreadable, create a separate note at `TaskNotes/Tasks/Tidy Review - [Note Title] - [Date].md` listing all questions, and embed a single comment in the note pointing to it:
```
%% TIDY: See [[Tidy Review - Note Title - Date]] for cleanup questions %%
```

---

## Step 4: Handle promoted fragments

For each fragment being promoted to a new note:

### New Task Note
Create at `TaskNotes/Tasks/[Inferred Title].md` using this format:
```yaml
---
status: do
priority: normal
dateCreated: [ISO8601]
dateModified: [ISO8601]
tags:
  - task
  - [additional inferred tags]
---

## Notes
[Original fragment content, cleaned up]
```

### New Concept Note
Create at `Zettlekasten/Concepts/[Concept Name].md`:
```yaml
---
date: YYYY-MM-DD
dateCreated: ISO8601
tags:
  - concept
  - [domain tags]
related:
  - "[[related concept or source]]"
---

# [Concept Name]

[Content, cleaned and structured]
```

### New Quote Note
Create at `Zettlekasten/Quotes/[Short Quote].md`:
```yaml
---
date: YYYY-MM-DD
dateCreated: ISO8601
tags:
  - quote
source: "[[Author or Book Note]]"
related: []
---

> [Full quote]

— [Attribution]

## Notes
[Any context or commentary]
```

### New Meeting Note
Create at `Meetings/[Date] - [Meeting Name].md` using the Meeting Template structure (status, priority, date, dateCreated, dateModified, tags: meeting, attendees, Agenda, Notes, Action Items sections).

### New People/Places/Organizations/Sources Note
Use the People Template for people. For other types, follow the frontmatter schema above, placing in the correct Zettlekasten subfolder.

### After creating each promoted note
In the original note, replace the promoted fragment with a wikilink:
```
[[Promoted Note Title]]
```

---

## Step 5: Commit the changes

After processing all notes, stage and commit to the cleanup branch:

```bash
VAULT="/Users/merc/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault"
cd "$VAULT"

# Stage all modified/new files from this cleanup
git add -A

git commit -m "$(cat <<'EOF'
tidy: cleanup pass on [note name(s)]

Notes processed: [list]
Promoted: [count] fragments to new notes
Questions embedded: [count]
EOF
)"
```

Then tell the user:
> Changes are staged on branch `cleanup/YYYY-MM-DD`. Open VSCode in the vault to review the diff:
> ```
> code "/Users/merc/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault"
> ```
> Switch to the Source Control panel (⌃⇧G) to review changes. When satisfied, merge the branch back to `main`. To respond to embedded `%% TIDY: ... %%` questions, edit the notes directly and then run `/tidy` again — it will detect your responses and apply the next round of changes.

---

## Step 6: Second-round — processing responses

If the user says they've responded to the `%% TIDY: ... %%` questions in the notes, do a second pass:

1. Read each note that had embedded questions
2. Find `%% TIDY: ... %%` blocks — look for user text added after "(reply here)"
3. Apply the appropriate action based on each response
4. Remove resolved `%% TIDY: ... %%` comments
5. Commit the second-round changes

For thematic or batch changes that aren't specific to one note (e.g., "move all meeting notes longer than X to the Meetings folder"), create a task note:

```
TaskNotes/Tasks/Tidy Thematic Changes - [Date].md
```

List the proposed changes there. The user can respond inline and you'll detect it in the next round.

---

## Zettlekasten folder structure

```
Zettlekasten/
  Concepts/         ← abstract ideas, principles, frameworks
  People/           ← individuals
  Places/           ← physical locations
  Organizations/    ← groups, institutions, companies, communities
  Quotes/           ← direct quotes with attribution
  Sources/
    Books/          ← book notes
    Articles/       ← web articles, newsletters, emails
    Videos/         ← YouTube, talks, podcasts
```

Note: vault uses the spelling `Zettlekasten` (not `Zettelkasten`).

---

## Inbox conventions

- `Inbox/` folder: truly homeless drafts with no clear category yet
- `#inbox` tag: notes already placed in their correct folder but not yet processed
- After a tidy pass, remove `#inbox` from tags

To find all unprocessed notes for a batch run:
```bash
grep -rl "#inbox" "/Users/merc/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault" \
  --include="*.md" | grep -v ".claude"
```

---

## Important constraints

- **Never commit to `main` directly** — always use a `cleanup/YYYY-MM-DD` branch
- **Never overwrite without a commit** — all changes must be in git before telling the user to review
- **Preserve the user's voice** — fix errors and structure, but don't rewrite their meaning or tone
- **Ask rather than assume** when classification is ambiguous — embed `%% TIDY: ... %%` comments
- **Daily notes**: do not add a Day Close section — that belongs to `/closeday`
- **Task notes**: title is the task description (imperative phrase), not a generic name
