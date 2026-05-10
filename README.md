# Process Tape 📼

A rough digital garden — a rolling log of things I build, fix, learn, and think about.

Not polished. Not a portfolio. Just the tape playing.

## Structure

- `entries.json` — main log, reverse-chronological entries
- `logs/YYYY-MM-DD.md` — daily auto-generated summaries

## Entry format

```json
{
  "date": "YYYY-MM-DD",
  "project": "project-name",
  "text": "what happened, in plain language",
  "tags": ["tag1", "tag2"]
}
```

Auto-updated daily by a cron job that reads session history and extracts meaningful work.
