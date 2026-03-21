# Image Collector Skill

Collects images sent to Justine via iMessage, Discord, and email — copies them to a central folder so Milo never loses track.

## How It Works

iMessage images land in `~/Library/Messages/Attachments/imsg/`. The skill watches this folder, copies new images to `~/.openclaw/workspace/received-images/`, and maintains a JSON manifest with timestamps and sources.

## Commands

### `new image` — Get Most Recent Image
Finds the newest image received via iMessage, copies it to `received-images/`, and reports what was found.

```bash
image-collector new
```

**What it does:**
1. Scans `~/Library/Messages/Attachments/imsg/` for image files (jpg, jpeg, png, gif, heic, webp,heif)
2. Finds the most recently modified file
3. Copies it to `~/.openclaw/workspace/received-images/` with a timestamp prefix (e.g., `2026-03-19_1025_img_001.jpg`)
4. Logs the file in `~/.openclaw/workspace/received-images/manifest.jsonl`
5. Returns the image path and a brief description

**Output format:**
```
New image saved:
  Path: ~/.openclaw/workspace/received-images/2026-03-19_1025_img_001.jpg
  Source: iMessage
  Original: IMG_4723.HEIC
  Size: 2.4 MB
```

### `list images` — List All Received Images
Lists all images in the `received-images/` folder with timestamps.

```bash
image-collector list
```

**Output format:**
```
Received images (sorted newest first):
  1. 2026-03-19 10:25 | 2026-03-19_1025_img_001.jpg | iMessage | 2.4 MB
  2. 2026-03-18 14:32 | 2026-03-18_1432_photo.png | iMessage | 1.1 MB
  3. 2026-03-17 09:11 | 2026-03-17_0911_screenshot.jpg | iMessage | 890 KB
```

### `peek image` — View Most Recent Without Copying
Just reports what's newest without touching anything.

```bash
image-collector peek
```

### `collect all` — Collect All Uncollected Images
Finds any images in the iMessage folder that haven't been copied yet and collects them all.

```bash
image-collector collect-all
```

## Technical Details

### File Storage
- **Destination:** `~/.openclaw/workspace/received-images/`
- **Naming:** `{date}_{time}_{original-name}.{ext}` — e.g., `2026-03-19_1025_IMG_4723.HEIC`
- **Manifest:** `~/.openclaw/workspace/received-images/manifest.jsonl` — one JSON line per image

### Manifest Entry Format
```json
{"collected_at":"2026-03-19T10:25:00-05:00","source":"imessage","original_name":"IMG_4723.HEIC","stored_name":"2026-03-19_1025_IMG_4723.HEIC","size_bytes":2500000,"path":"~/.openclaw/workspace/received-images/2026-03-19_1025_IMG_4723.HEIC"}
```

### iMessage Attachment Path
`~/Library/Messages/Attachments/imsg/`

Supports all common image formats: `jpg`, `jpeg`, `png`, `gif`, `heic`, `heic`, `webp`, `tiff`, `bmp`

### Source Priority
When multiple images have the same timestamp, prefer by source order:
1. `imessage` (highest priority — most common for Justine)
2. `discord` (future-proofing)
3. `email` (future-proofing)

## Error Handling
- Missing attachment folder → exit 1 with clear message
- No images found → "No images found in iMessage attachments"
- Permission denied → hint to grant Full Disk Access
- Corrupt file → skip and log, continue with next

## Permissions Required
- **Full Disk Access** (System Preferences → Privacy & Security → Full Disk Access)
- Required to read `~/Library/Messages/`

## Cron Integration (Optional)
To auto-collect every 5 minutes, add to crontab:
```
*/5 * * * * /Users/justinedelano/.openclaw/skills/image-collector/image-collector.sh collect-all >> ~/.openclaw/logs/image-collector.log 2>&1
```

Or use OpenClaw's built-in cron (preferred — less permission issues).

## Files
```
~/.openclaw/skills/image-collector/
  SKILL.md                          ← this file
  image-collector.sh               ← the script

~/.openclaw/workspace/received-images/
  2026-03-19_1025_IMG_4723.HEIC    ← collected images
  manifest.jsonl                    ← history log
```
