---
name: video-capture
description: Archive a YouTube/Shorts/Facebook Reel/TikTok-style video offline in the vault with real metadata (author, transcript, summary), an improved title, and a link to whatever vault note it's relevant to. Use whenever Alex pastes one or more video links he wants to keep, not just bookmark — exercise/rehab videos are the most common case, but this applies to any topic.
---

# /video-capture

Alex can't reliably view YouTube Shorts / Facebook Reels / similar short-form video without Wi-Fi, and platform titles ("28K views · 912 reactions | Here is the mobility routine...") are useless for search later. When he drops video links, they get downloaded, cataloged with real metadata, and linked into the vault — not just bookmarked.

## When to use

Trigger whenever Alex pastes one or more short-form video links (YouTube Shorts, `youtube.com/watch`, Facebook Reels, `facebook.com/share/...`, or similar) that he clearly wants to keep — often with a short label or a note about why ("ask Mario about this drill", "this explains the thing I was describing"). Don't wait for him to spell out the full process; this skill **is** the spelled-out process, for any subject matter.

**This is a general capture skill.** The topic/folder is whatever the content is about — exercise videos go under `Physio Exercises`, a cooking technique might go under `Cooking`, a theology lecture under its own topic folder, etc. Infer the topic folder name from context (what note(s) the video relates to, or what Alex calls it); ask if genuinely ambiguous. Check whether a `Zettelkasten/Sources/<Topic>/` folder already exists for this subject before creating a new one.

## Why this exists, not just a bookmark

1. **Offline access.** The core reason — these need to play without Wi-Fi.
2. **Legal/ToS.** Claude does not bulk-download YouTube/Facebook content itself (ToS risk at scale). Alex downloads via **Downie** (a legitimate personal-archival tool he already owns); Claude's job is the clipboard handoff, verification, and cataloging.
3. **Findability.** Every video gets a real, descriptive, content-accurate title — not the platform's auto-generated one.
4. **Context survives.** Months later, "why do I have this" and "who made this" should be answerable without re-watching — hence real author attribution, a summary, and a transcript.

## Process

### 1. Collect URLs

Gather every video URL from the message (and, if the user references an existing note, any bare video URLs already sitting there as unprocessed bullets). Dedupe. If more than a couple of links, copy the full list to the clipboard (`pbcopy`) for the user to hand off to Downie themselves — don't ask them to click each link one by one.

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

(ZDATE is a Core Data timestamp — seconds since 2001-01-01, hence the `+ 978307200` offset to convert to Unix epoch.) This gives the exact source URL and the full on-screen caption/title per download, which filenames alone often truncate or garble.

If a share link still won't resolve to a confirmable match, say so explicitly and flag the note with an inline `> [!warning] Unconfirmed match` callout rather than silently guessing — see [[Zettelkasten/Sources/Physio Exercises/Maintaining External Rotation]] for the pattern. Ask the user to re-share the specific link if it matters.

Also watch for **autoplay bleed**: opening one Facebook Reel can cause Downie to grab several "up next" reels too. Don't assume a 1:1 match between URLs given and files downloaded without checking.

### 3. Pull real metadata with `yt-dlp` — don't guess, don't default to "unknown"

Install once if missing: `brew install yt-dlp`. This works on both YouTube and Facebook and is the single biggest accuracy win in this whole process — use it even though Downie already fetched the video:

```bash
yt-dlp --dump-json --skip-download "<url>"
```

Pull from the JSON:
- **`uploader` / `channel`** → the `author` frontmatter field. This is almost always present and correct — there is no excuse for writing `author: unknown` when this field returns a real name. (Past mistake: notes were written with `author: unknown` even when the creator's name was sitting in the platform caption text, e.g. "Elitzur Bergman DPT" — don't repeat this.)
- **`description`** → useful for Facebook reels, which often have no spoken dialogue but a full creator-written caption here.
- **`automatic_captions`** → see step 5, this is the real transcript source.

If `yt-dlp` genuinely returns nothing for author (rare), fall back to on-screen caption attribution (e.g. a page name visible in the video) before writing `unknown`.

### 4. Write an improved title

Never keep the platform's auto-generated filename/title (view counts, hashtag soup, clickbait phrasing like "She Didn't Want ROUNDED SHOULDERS!😩"). Write a short, descriptive, content-accurate title a future search would actually find — e.g. "Fix Your Shoulder Mobility" → **"Shoulder Protraction Without Scapular Winging"**. This title becomes both the note filename and the video filename (keep them byte-for-byte identical, including any `.srt` sidecar — a filename typo here breaks the `![[...]]` embed silently, since Obsidian doesn't error on a dangling embed, it just renders nothing playable).

### 5. Get a real transcript — prefer `yt-dlp` auto-captions over Downie's bundled `.srt`

```bash
yt-dlp --write-auto-sub --sub-lang en --skip-download -o "<title>.%(ext)s" "<url>"
```

This works for **both** YouTube and Facebook (Facebook reels often do have speech-to-text captions available even though Downie doesn't fetch them) and is more reliable than relying on whatever Downie happened to bundle. Platform quirks:
- YouTube: request `--sub-lang "en,en-orig"` (auto-generated captions sometimes only exist under the `en-orig` tag).
- Facebook: request `--sub-lang en_US` specifically — plain `en` often returns nothing even when captions exist.
- Requesting multiple comma-separated langs where none match can silently return nothing on some extractors; if a single combined request comes back empty, retry each lang code separately before concluding there's no transcript.
- Rate limits: YouTube will 429 after rapid-fire requests across many videos in one session — space batch requests a few seconds apart.

Convert the downloaded `.vtt`/`.srt` into clean prose for the `## Transcript` section (merge overlapping/duplicate caption fragments — don't paste raw timestamped captions).

**If no captions exist at all** (silent clips, non-English speech, STT genuinely unavailable): use the creator's own caption/description text (from step 3's `description` field) under `## Transcript`, explicitly noting *"No spoken-word transcript available — using the creator's on-screen caption:"* followed by a blockquote. Don't fabricate a spoken transcript. No local STT fallback tool (whisper, etc.) is installed as of 2026-10 — ask before installing one if captions-via-yt-dlp comes back empty.

### 6. Move files into the vault

```
Attachments/<Topic>/<Improved Title>.<ext>        (video; keep original extension — mp4/mkv/etc.)
Attachments/<Topic>/<Improved Title>.srt          (transcript sidecar, if kept)
```

**Do not `git add` the video/srt files** — they're iCloud-synced only, matching this vault's existing large-file convention (no LFS, no git tracking for media; the vault's blanket "ignore everything but markdown" `.gitignore` already excludes media extensions). Only the `.md` source note is version-controlled.

**After moving, verify the embed resolves** — don't trust that the move succeeded just because the shell command didn't error:

```bash
ls "Attachments/<Topic>/<Improved Title>.<ext>"
```

(Past bug: `shutil.move` between two different iCloud Drive ubiquity containers silently no-op'd for several files in one batch, and separately a title/extension mismatch left 6 notes embedding a `.srt` file where a video was intended, rendering as unplayable text instead of video. Always spot-check a sample of the actual `![[...]]` targets against the real directory listing, not just the move command's exit code.)

### 7. Write the source note

Location: `Zettelkasten/Sources/<Topic>/<Improved Title>.md`. Based on `Templates/Source Note Template.md`, extended with Summary + Transcript:

```markdown
---
title: <Improved Title>
source: <original URL>
originalTitle: <platform's original title/caption, if materially different>
type: video
author: <real creator/channel/page name from yt-dlp — see step 3>
dateCaptured: <YYYY-MM-DD>
tags:
  - source
  - <topic-tag, e.g. physio-exercise>
---

# <Improved Title>

## Why I have this

- <one line: what this is and why it was kept — link to the relevant vault note(s)>

## Summary

<2-4 sentences: what the video actually shows/explains>

## Transcript

<cleaned transcript, or caption fallback per step 5>

## Video

![[<Improved Title>.<ext>]]

## Related

- [[<relevant vault note(s)>]]
```

If there's no obviously relevant vault note to link, that's fine — not every capture needs a `## Related` target. Don't invent a connection that isn't there.

### 8. Link from the relevant note, if one exists

Add or extend an "Exercise library" / "Video library" / similarly-named section in whatever note(s) this relates to, with a wikilink to the new source note. If that note already has a bare URL for this exact video (common — these notes often start as a raw link dump), **replace the bare URL with the wikilink** rather than leaving both.

### 9. Format, commit, push

```bash
npx --yes prettier --write "<related note(s)>" "Zettelkasten/Sources/<Topic>/<new note(s)>.md"
git add "<related note(s)>" "Zettelkasten/Sources/<Topic>/<new note(s)>.md"
git commit -m "..."
git push origin main && git push github main
```

**Established exception for this workflow**: commit straight to `main` in the iCloud vault, no feature branch/PR. Alex approved this explicitly (2026-09-29) for the physio-exercise case specifically, on the reasoning that these are append-only cataloging notes with no real review value, and branching is impractical given the binary volume involved in a typical batch. Apply the same reasoning for other topics unless a given capture is large/contentious enough to warrant review — when in doubt, it's a quick check-in, not a blocker. This does **not** generalize to other vault work; see `AGENTS.md § Git Workflow` for the default branch+PR policy everywhere else.

If a push hangs or times out, retry once before escalating — this vault's git remotes occasionally have transient hiccups unrelated to the actual state (see [[2026-09-29 Physio Exercise Video Archive]] for a worked example).

### 10. Log it

A short daily-log bullet pointing at the relevant note (or a work session note, if it's a sizeable batch) — per `.claude/work-session-notes.md`. Don't skip this even for a two-video addition; the stop-hook session-doc-check will catch it if you do.

## Worked example: physio exercise videos

The first (and so far only) applied domain: exercise/rehab videos tied to [[Shoulder Instability]] and [[Body asymmetry]], archived in `Zettelkasten/Sources/Physio Exercises/` / `Attachments/Physio Exercises/`, tagged `physio-exercise`. 39 videos as of 2026-10-01. Check there first for anything shoulder/asymmetry-related — a video may already be captured under a different label.

## Known gaps / open questions

- No local STT fallback tool installed — if `yt-dlp` auto-captions come back empty for a video, the creator's caption/description text is used instead of a real transcript. Ask before installing something like whisper.cpp to close this gap.
- `yt-dlp` needs periodic `brew upgrade yt-dlp` — platform extractors break often as YouTube/Facebook change their internals.
