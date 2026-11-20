#!/usr/bin/env python3
# prune_backups.py
import sys
from datetime import datetime, timedelta, UTC
from pathlib import Path

KEEP = timedelta(days=7)


def main(directory):
    cutoff = datetime.now(UTC) - KEEP
    for path in Path(directory).glob("*.tar.gz"):
        modified = datetime.fromtimestamp(path.stat().st_mtime, UTC)
        if modified < cutoff:
            print(f"deleting {path} (modified {modified:%Y-%m-%d})")
            path.unlink()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"usage: python3 {sys.argv[0]} BACKUP_DIR")
    main(sys.argv[1])
