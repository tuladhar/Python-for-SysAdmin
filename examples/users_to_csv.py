#!/usr/bin/env python3
# users_to_csv.py
import csv
import sys

fields = ["user", "password", "uid", "gid", "comment", "home", "shell"]

with open("/etc/passwd", newline="", encoding="utf-8") as f:
    users = [dict(zip(fields, row)) for row in csv.reader(f, delimiter=":", quoting=csv.QUOTE_NONE)]

writer = csv.DictWriter(sys.stdout, fieldnames=["user", "uid", "home", "shell"],
                        extrasaction="ignore")
writer.writeheader()
writer.writerows(u for u in users if int(u["uid"]) >= 1000)
