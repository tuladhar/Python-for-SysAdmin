#!/usr/bin/env python3
# line_count.py
import fileinput

lines = 0
for line in fileinput.input(encoding="utf-8"):
    lines += 1

print("total lines:", lines)
