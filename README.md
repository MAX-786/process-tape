# Process Tape 📼

A rough digital garden — a rolling log of things I build, fix, learn, and think about.

Not polished. Not a portfolio. Just the tape playing.

---

## Structure

```
process-tape/
├── entries.json          # manual dev log entries
├── meta.json             # auto-generated index (projects, tags, dates, counts)
├── logs/
│   └── YYYY-MM-DD.json  # daily auto-summaries written by cron
├── scripts/
│   └── build_meta.py    # regenerates meta.json from entries.json
└── SCHEMA.md             # full data spec
```

---

## Entry format

Each entry in `entries.json` is one atomic thought, change, or decision:

```json
{
  "id": "entry-YYYYMMDD-001",
  "date": "YYYY-MM-DD",
  "project": "project-slug",
  "text": "what happened, in plain language",
  "tags": ["tag1", "tag2"]
}
```

---

## Daily logs

Every night at ~5 AM IST, a cron job scans the day's work and writes a structured summary to `logs/YYYY-MM-DD.json`:

```json
{
  "date": "YYYY-MM-DD",
  "generated_at": "...",
  "projects_touched": ["project-a"],
  "summary": "What the day was about.",
  "highlights": ["thing done", "decision made"],
  "tags": ["tag1", "tag2"]
}
```

---

## Fetching data (for a frontend)

All files are static JSON — no backend needed. Fetch directly from raw GitHub:

```
https://raw.githubusercontent.com/MAX-786/process-tape/main/entries.json
https://raw.githubusercontent.com/MAX-786/process-tape/main/meta.json
https://raw.githubusercontent.com/MAX-786/process-tape/main/logs/YYYY-MM-DD.json
```

Use `meta.json` for fast index data (projects, tags, date range) without parsing all entries.

---

## Regenerating meta

After editing `entries.json` manually, run:

```bash
python scripts/build_meta.py
```

See [SCHEMA.md](./SCHEMA.md) for the full data spec.
