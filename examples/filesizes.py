#!/usr/bin/env python3
# filesizes.py
import os
import sys


def filesizes(path):
    """Print the size in bytes of each file under path."""
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                size = os.path.getsize(filepath)
            except OSError:
                continue  # broken symlink or file removed meanwhile
            print(f"{size:>10} {filepath}")


def main(argv):
    if len(argv) != 1:
        sys.exit(f"usage: python3 {sys.argv[0]} DIR")
    filesizes(argv[0])


if __name__ == "__main__":
    main(sys.argv[1:])
