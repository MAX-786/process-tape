#!/usr/bin/env python3
"""
build_meta.py
Regenerates meta.json from entries.json.
Run after manually editing entries.json.
"""

import json
import os
from datetime import datetime, timezone
from collections import defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRIES_FILE = os.path.join(REPO, "entries.json")
META_FILE = os.path.join(REPO, "meta.json")


def build_meta():
    with open(ENTRIES_FILE) as f:
        entries = json.load(f)

    if not entries:
        print("No entries found.")
        return

    # Collect per-project data
    projects = defaultdict(lambda: {"entry_count": 0, "last_active": "", "tags": set()})
    all_tags = set()
    all_dates = set()

    for entry in entries:
        date = entry["date"]
        project = entry["project"]
        tags = entry.get("tags", [])

        projects[project]["entry_count"] += 1
        if date > projects[project]["last_active"]:
            projects[project]["last_active"] = date
        projects[project]["tags"].update(tags)
        all_tags.update(tags)
        all_dates.add(date)

    sorted_dates = sorted(all_dates, reverse=True)

    meta = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_entries": len(entries),
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
            "first": sorted_dates[-1],
            "last": sorted_dates[0],
        },
        "days": sorted_dates,
    }

    with open(META_FILE, "w") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")

    print(f"meta.json updated: {len(entries)} entries, {len(all_dates)} days, {len(projects)} projects")


if __name__ == "__main__":
    build_meta()
