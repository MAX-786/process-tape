# Process Tape — Data Schema

All data lives in this repo as static JSON. No backend required.
A frontend can fetch files directly from raw GitHub or any static host.

---

## `entries.json`

The main log. An array of individual work entries, sorted newest-first.

```json
[
  {
    "id": "entry-YYYYMMDD-NNN",     // unique ID: date + sequence number
    "date": "YYYY-MM-DD",           // ISO 8601 date (UTC)
    "project": "project-slug",      // short kebab-case project name
    "text": "what happened",        // plain language, first-person, informal
    "tags": ["tag1", "tag2"]        // lowercase or camelCase, freeform
  }
]
```

**Rules:**
- One entry = one atomic thought/change/decision. Not a full day summary.
- `id` format: `entry-{YYYYMMDD}-{000}` — zero-padded 3-digit sequence per day
- `tags` are freeform — no controlled vocabulary, just whatever is useful
- Entries are manually authored or auto-appended by the cron job
- Always sorted newest → oldest

---

## `logs/YYYY-MM-DD.json`

Auto-generated daily summary for each active day (created by cron).
One file per day. Only days with activity get a file.

```json
{
  "date": "YYYY-MM-DD",
  "generated_at": "ISO 8601 datetime",
  "entry_ids": ["entry-YYYYMMDD-001", "entry-YYYYMMDD-002"],
  "projects_touched": ["project-a", "project-b"],
  "summary": "Short paragraph — what the day was about overall.",
  "highlights": [
    "bullet: key thing done",
    "bullet: key decision made"
  ],
  "tags": ["all", "tags", "from", "day"]
}
```

---

## `meta.json`

Auto-regenerated every time entries change. Provides fast index data
without parsing all entries — useful for sidebars, filters, stats.

```json
{
  "generated_at": "ISO 8601 datetime",
  "total_entries": 42,
  "total_days": 17,
  "projects": [
    {
      "name": "project-slug",
      "entry_count": 10,
      "last_active": "YYYY-MM-DD",
      "tags": ["all", "unique", "tags"]
    }
  ],
  "all_tags": ["sorted", "unique", "tag", "list"],
  "date_range": {
    "first": "YYYY-MM-DD",
    "last": "YYYY-MM-DD"
  },
  "days": ["YYYY-MM-DD", "..."]    // all dates with at least one entry, newest-first
}
```

---

## `scripts/build_meta.py`

Run locally (or in CI) to regenerate `meta.json` after editing `entries.json`.

```
python scripts/build_meta.py
```

---

## Fetching from a frontend

Raw GitHub URLs (replace `main` with your branch):

```
https://raw.githubusercontent.com/MAX-786/process-tape/main/entries.json
https://raw.githubusercontent.com/MAX-786/process-tape/main/meta.json
https://raw.githubusercontent.com/MAX-786/process-tape/main/logs/2026-05-10.json
```

Or use the GitHub Contents API if you need directory listings:
```
https://api.github.com/repos/MAX-786/process-tape/contents/logs
```
