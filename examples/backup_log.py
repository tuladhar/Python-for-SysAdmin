#!/usr/bin/env python3
# backup_log.py
import sqlite3
import sys
from datetime import datetime, UTC

con = sqlite3.connect("backups.db")
con.execute("""
    CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY,
        started TEXT NOT NULL,
        target TEXT NOT NULL,
        ok INTEGER NOT NULL
    )
""")

if len(sys.argv) == 3:
    # record a run:  python3 backup_log.py /srv/data ok
    target, status = sys.argv[1], sys.argv[2]
    with con:
        con.execute(
            "INSERT INTO runs (started, target, ok) VALUES (?, ?, ?)",
            (datetime.now(UTC).isoformat(timespec="seconds"), target, status == "ok"),
        )

# report the last 5 runs
for started, target, ok in con.execute(
    "SELECT started, target, ok FROM runs ORDER BY id DESC LIMIT 5"
):
    print(f"{started}  {'OK  ' if ok else 'FAIL'}  {target}")

con.close()
