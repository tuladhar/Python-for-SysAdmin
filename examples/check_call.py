#!/usr/bin/env python3
# check_call.py
import subprocess
import sys

cmd = ["ls", "/no/such/dir"]
print("running command:", " ".join(cmd))

try:
    subprocess.run(cmd, check=True, capture_output=True, text=True)
except subprocess.CalledProcessError as e:
    sys.exit(f"error: exit code {e.returncode}: {e.stderr.strip()}")
