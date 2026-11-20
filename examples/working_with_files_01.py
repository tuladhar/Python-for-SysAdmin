#!/usr/bin/env python3
# working_with_files_01.py
import sys


def main():
    try:
        with open("/etc/passwd", encoding="utf-8") as f:
            for no, line in enumerate(f, start=1):
                if line.rstrip().endswith("/bin/bash"):
                    print(f"{no} {line.rstrip()}")
    except OSError as e:
        sys.exit(f"error: {e}")


if __name__ == "__main__":
    main()
