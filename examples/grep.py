#!/usr/bin/env python3
# grep.py
import sys


def main(argv):
    if len(argv) != 1:
        sys.exit(f"usage: python3 {sys.argv[0]} PATTERN")

    pattern = argv[0]
    for line in sys.stdin:
        if pattern in line:
            print(line.rstrip())


if __name__ == "__main__":
    main(sys.argv[1:])
