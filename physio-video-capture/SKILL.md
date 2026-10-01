---
name: physio-video-capture
description: Archive exercise/rehab videos (YouTube Shorts, Facebook Reels) offline in the vault with a transcript, summary, improved title, and links back to the relevant body-issue note. Use when Alex pastes one or more exercise video links, often tied to an ongoing physical issue (e.g. shoulder instability, body asymmetry).
---

# /physio-video-capture

Alex can't reliably view YouTube Shorts / Facebook Reels without Wi-Fi, so exercise videos he collects get downloaded, cataloged, and linked into the vault for offline access — not just bookmarked.

## When to use

Trigger whenever Alex pastes one or more video links (YouTube Shorts, `youtube.com/watch`, Facebook Reels, `facebook.com/share/...`) alongside a short label or context clue tying it to a body issue — e.g. "shoulder staff exercises", "hip warmup", "ask Mario about this drill". Don't wait for him to spell out the full process; this skill **is** the spelled-out process.

Existing archive: `Zettelkasten/Sources/Physio Exercises/` (37+ notes as of 2026-10-01), linked from [[Shoulder Instability]] and [[Body asymmetry]]. Check there first — a video may already be captured under a different label.

## Why this exists, not just a bookmark

1. **Offline access.** The whole point — these need to play without Wi-Fi.
2. **Legal/ToS.** Claude does not bulk-download YouTube/Facebook content itself (ToS risk at scale). Alex downloads via **Downie** (a legitimate personal-archival tool he already owns); Claude's job is the clipboard handoff, verification, and cataloging.
3. **Findability.** Platform titles are useless for search later ("28K views · 912 reactions | Here is the mobility routine..."). Every video gets a real, descriptive title.
4. **Context survives.** Six months from now, "why do I have this video" should be answerable without re-watching it — hence the why-I-have-this line, summary, and transcript.

## Process

### 1. Collect URLs

Gather every video URL from the message (and, if the user references an existing note, any bare video URLs already sitting in that note as unprocessed bullets). Dedupe. If more than a couple of links, copy the full list to the clipboard (`pbcopy`) for the user to hand off to Downie themselves — don't ask them to click each link one by one.

### 2. Confirm the download landed

Downie's save folder is **`~/Library/Mobile Documents/com~apple~CloudDocs/Downloads/`** (an iCloud Drive folder, not `~/Downloads`). Check there for new files:

```bash
find "$HOME/Library/Mobile Documents/com~apple~CloudDocs/Downloads" -maxdepth 1 -newermt "<session start time>" -type f
```

If Downie crashed mid-batch or the file count doesn't match the URL count, cross-reference **Downie's history database** rather than guessing from filenames — Facebook rewrites `share/r/...`/`share/v/...` links on resolution, so the saved filename often won't obviously match the original URL:

```bash
sqlite3 "$HOME/Library/Containers/com.charliemonroe.Downie-setapp/Data/Library/Application Support/com.charliemonroe.Downie-setapp/History.db" \
  "SELECT datetime(ZDATE + 978307200, 'unixepoch','localtime'), ZORIGINALWEBSITEURLSTRING, ZTITLE FROM ZXUCOMPLETEDDOWNLOAD ORDER BY ZDATE DESC LIMIT 20;"
```

(ZDATE is a Core Data timestamp — seconds since 2001-01-01, hence the `+ 978307200` offset to convert to Unix epoch.) This gives the exact source URL and full on-screen caption/title per download, which filenames alone often truncate or garble.

If a Facebook share link still won't resolve to a confirmable match, say so explicitly and flag the note with an inline `> [!warning] Unconfirmed match` callout rather than silently guessing — see [[Zettelkasten/Sources/Physio Exercises/Maintaining External Rotation]] for the pattern. Ask the user to re-share the specific link if it matters.

Also watch for **autoplay bleed**: opening one Facebook Reel can cause Downie to grab several "up next" reels too. Don't assume a 1:1 match between URLs given and files downloaded without checking.

### 3. Write an improved title

Never keep the platform's auto-generated filename/title (view counts, hashtag soup, clickbait phrasing like "She Didn't Want ROUNDED SHOULDERS!😩"). Write a short, descriptive, content-accurate title a future search would actually find — e.g. "Fix Your Shoulder Mobility" → **"Shoulder Protraction Without Scapular Winging"**. This title becomes both the note filename and the video filename (keep them identical, including the `.srt` sidecar if one exists).

### 4. Move files into the vault

```
Attachments/Physio Exercises/<Improved Title>.<ext>        (video; keep original extension — mp4/mkv/etc.)
Attachments/Physio Exercises/<Improved Title>.srt          (if Downie produced captions)
```

**Do not `git add` the video/srt files** — they're iCloud-synced only, matching this vault's existing large-file convention (no LFS, no git tracking for media; see `Attachments/.gitignore` behavior — media extensions are already excluded by the vault's blanket "ignore everything but markdown" `.gitignore`). Only the `.md` source note is version-controlled.

### 5. Get a transcript

- If Downie produced a `.srt` (YouTube auto-captions), merge the overlapping caption fragments into clean prose for the `## Transcript` section — don't paste raw timestamped SRT.
- If there's no `.srt` (Facebook reels rarely get auto-captions), use the creator's own on-screen caption text (available via the `ZTITLE` column in Downie's history DB, often truncated in the filename but full-length in the DB) under a `## Transcript` heading, explicitly noting: *"No spoken-word transcript available — Facebook doesn't auto-caption this reel. On-screen caption (creator's own text):"* followed by a blockquote. Don't fabricate a spoken transcript.
- No local speech-to-text tool is currently installed (checked: no `whisper`/`whisper-cli`/`mlx_whisper` in PATH, only `ffmpeg`). If Alex wants real transcripts for caption-less videos, that requires installing a local STT tool first — ask, don't install silently.

### 6. Write the source note

Location: `Zettelkasten/Sources/Physio Exercises/<Improved Title>.md`. Based on `Templates/Source Note Template.md`, extended with Summary + Transcript:

```markdown
---
title: <Improved Title>
source: <original URL>
originalTitle: <platform's original title/caption, if materially different>
type: video
author: <creator/page name, or "unknown">
dateCaptured: <YYYY-MM-DD>
tags:
  - source
  - physio-exercise
---

# <Improved Title>

## Why I have this

- <one line: what this exercise targets, and which condition note it's for>

## Summary

<2-4 sentences: what the exercise/drill is, the cue or principle it teaches>

## Transcript

<cleaned transcript or on-screen-caption fallback, per step 5>

## Video

![[<Improved Title>.<ext>]]

## Related

- [[<condition note, e.g. Shoulder Instability>]]
```

### 7. Link from the condition note

Add or extend an `## Exercise library` section in the relevant condition note(s) (e.g. [[Shoulder Instability]], [[Body asymmetry]]) with a wikilink to the new source note. If the condition note already has a bare URL for this exact video (common — these notes often start as a raw link dump), **replace the bare URL with the wikilink** rather than leaving both.

### 8. Format, commit, push

```bash
npx --yes prettier --write "<condition note(s)>" "Zettelkasten/Sources/Physio Exercises/<new note(s)>.md"
git add "<condition note(s)>" "Zettelkasten/Sources/Physio Exercises/<new note(s)>.md"
git commit -m "..."
git push origin main && git push github main
```

**Established exception for this workflow**: commit straight to `main` in the iCloud vault, no feature branch/PR. Alex approved this explicitly (2026-09-29) for this recurring task specifically — these are append-only cataloging notes with no real review value, and branching is impractical given the binary volume involved in a typical batch. This does **not** generalize to other vault work; see `AGENTS.md § Git Workflow` for the default branch+PR policy everywhere else.

If a push hangs or times out, retry once before escalating — this vault's git remotes occasionally have transient hiccups unrelated to the actual state (see [[2026-09-29 Physio Exercise Video Archive]] for a worked example).

### 9. Log it

A short daily-log bullet pointing at the condition note (or a work session note, if it's a sizeable batch) — per `.claude/work-session-notes.md`. Don't skip this even for a two-video addition; the stop-hook session-doc-check will catch it if you do.

## Known gaps / open questions

- No local STT tool yet — Facebook reels without creator captions get the on-screen-caption fallback, not a real transcript, until one's installed.
- The original 2026-09-29 batch (35 videos) predates the transcript/summary requirement — those notes only have a "why I have this" line. Backfilling them with transcripts is a separate, larger task; ask before taking it on rather than assuming scope.
