#!/usr/bin/env python3
# stopped_containers.py
import json
import subprocess

result = subprocess.run(
    ["docker", "ps", "-a", "--format", "json"],
    check=True, capture_output=True, text=True,
)

for line in result.stdout.splitlines():
    container = json.loads(line)
    if container["State"] != "running":
        print(f"{container['Names']:<30} {container['Status']}")
