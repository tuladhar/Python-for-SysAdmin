#!/usr/bin/env python3
# argv_02.py
import sys

args = sys.argv[1:]  # drop the script name

if len(args) != 2:
    sys.exit(f"invalid number of arguments (expected 2, given: {len(args)})")

print("two arguments are:", args)
