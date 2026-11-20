#!/usr/bin/env python3
# stdio.py
import sys

# write to stdout
print("Hello, world")
sys.stdout.write("Hello, world\n")

# write to stderr
print("Something went wrong", file=sys.stderr)
sys.stderr.write("Something went wrong\n")

# read a single line from stdin
username = input("Username: ")
print(f"Hi, {username}")

# read everything until EOF (press Ctrl-D in a terminal)
print("Enter a few lines and press Ctrl-D", file=sys.stderr)
lines = sys.stdin.readlines()
print("total lines read:", len(lines))
