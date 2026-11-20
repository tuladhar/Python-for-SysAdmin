#!/usr/bin/env python3
# follow.py
import subprocess

with subprocess.Popen(
    ["ping", "-c", "5", "1.1.1.1"],
    stdout=subprocess.PIPE,
    text=True,
) as proc:
    for line in proc.stdout:
        print("ping says:", line.rstrip())

print("exit code:", proc.returncode)
