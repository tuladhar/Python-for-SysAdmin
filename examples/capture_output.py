#!/usr/bin/env python3
# capture_output.py
import subprocess
import sys
from pathlib import Path

cmd = ["cat", "/etc/hosts"]
print("running command:", " ".join(cmd))

try:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
except subprocess.CalledProcessError as e:
    sys.exit(f"error: {e.stderr}")

Path("hosts.txt").write_text(result.stdout, encoding="utf-8")
print("success! wrote", len(result.stdout), "characters to hosts.txt")
