#!/usr/bin/env python3
# sys_01.py
import sys

print(f"Python version: {sys.version}")
print(f"Running on platform: {sys.platform}")
print(f"Interpreter: {sys.executable}")

if len(sys.argv) > 10:
    sys.exit("error: too many arguments")

print(f"argv = {sys.argv}")
print("Printing to stdout")
print("Printing to stderr", file=sys.stderr)

print(f"module search paths: {len(sys.path)}")
print(f"modules loaded: {len(sys.modules)}")

sys.exit(0)  # success
