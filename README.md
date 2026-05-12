# Process Tape 📼

A rough digital garden — a rolling log of things I build, fix, learn, and think about.

Not polished. Not a portfolio. Just the tape playing.

---

## Structure

```
process-tape/
├── logs/
│   └── YYYY-MM-DD.json  # daily auto-summaries written by cron (source of truth)
├── meta.json             # auto-generated index (projects, tags, dates, counts)
├── scripts/
│   └── build_meta.py    # regenerates meta.json from logs/
└── SCHEMA.md             # full data spec
```

> `entries.json` has been removed. `logs/` is the single source of truth.

---

## Daily log format

Every night at ~5 AM IST, a cron job scans the day's work and writes a structured summary to `logs/YYYY-MM-DD.json`:

```json
{
  "date": "YYYY-MM-DD",
  "generated_at": "...",
  "projects_touched": ["project-a", "project-b"],
  "summary": "What the day was about, in plain language.",
  "highlights": ["thing done", "decision made"],
  "tags": ["tag1", "tag2"]
}
```

---

## Fetching data (for a frontend)

All files are static JSON — no backend needed.

```
# Index (start here — contains the full ordered list of dates)
https://raw.githubusercontent.com/MAX-786/process-tape/main/meta.json

# Individual day log
https://raw.githubusercontent.com/MAX-786/process-tape/main/logs/YYYY-MM-DD.json
```

`meta.json` contains a `days` array (newest-first) you can use to paginate over log files without listing the directory.

---

## Regenerating meta

After new logs are added or to rebuild from scratch:

```bash
python scripts/build_meta.py
```

This walks all `logs/*.json` files and regenerates `meta.json` with aggregated project stats, tag lists, and date ranges.

See [SCHEMA.md](./SCHEMA.md) for the full data spec.
