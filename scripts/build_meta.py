#!/usr/bin/env python3
"""
build_meta.py
Regenerates meta.json from logs/ folder (YYYY-MM-DD.json files).
Run after new logs are added, or manually to rebuild.
"""

import json
import os
from datetime import datetime, timezone
from collections import defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(REPO, "logs")
META_FILE = os.path.join(REPO, "meta.json")


def build_meta():
    if not os.path.isdir(LOGS_DIR):
        print("No logs/ directory found.")
        return

    log_files = sorted(
        [f for f in os.listdir(LOGS_DIR) if f.endswith(".json")],
        reverse=True,  # newest first
    )

    if not log_files:
        print("No log files found in logs/.")
        return

    # Collect per-project data across all daily logs
    projects = defaultdict(lambda: {"entry_count": 0, "last_active": "", "tags": set()})
    all_tags = set()
    all_dates = []

    for filename in log_files:
        filepath = os.path.join(LOGS_DIR, filename)
        try:
            with open(filepath) as f:
                log = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"Skipping {filename}: {e}")
            continue

        date = log.get("date", filename.replace(".json", ""))
        tags = log.get("tags", [])
        touched = log.get("projects_touched", [])

        all_dates.append(date)
        all_tags.update(tags)

        for project in touched:
            projects[project]["entry_count"] += 1
            if date > projects[project]["last_active"]:
                projects[project]["last_active"] = date
            projects[project]["tags"].update(tags)

    sorted_dates = sorted(all_dates, reverse=True)

    meta = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_entries": len(all_dates),
        "total_days": len(all_dates),
        "projects": sorted(
            [
                {
                    "name": name,
                    "entry_count": data["entry_count"],
                    "last_active": data["last_active"],
                    "tags": sorted(data["tags"]),
                }
                for name, data in projects.items()
            ],
            key=lambda p: p["last_active"],
            reverse=True,
        ),
        "all_tags": sorted(all_tags),
        "date_range": {
            "first": sorted_dates[-1] if sorted_dates else "",
            "last": sorted_dates[0] if sorted_dates else "",
        },
        "days": sorted_dates,  # newest-first — API uses this for pagination
    }

    with open(META_FILE, "w") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")

    print(
        f"meta.json updated: {len(all_dates)} days, "
        f"{len(projects)} projects, "
        f"{len(all_tags)} tags"
    )


if __name__ == "__main__":
    build_meta()
