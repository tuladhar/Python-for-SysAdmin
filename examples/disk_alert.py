#!/usr/bin/env python3
# disk_alert.py
import shutil
import sys

THRESHOLD = 80  # percent


def main(path="/"):
    total, used, free = shutil.disk_usage(path)
    percent = used / total * 100
    print(f"{path}: {percent:.1f}% used, {free / 2**30:.1f} GiB free")
    if percent > THRESHOLD:
        # a non-zero exit code lets cron, systemd or your monitoring react
        sys.exit(f"WARNING: {path} is above {THRESHOLD}%")


if __name__ == "__main__":
    main(*sys.argv[1:])
