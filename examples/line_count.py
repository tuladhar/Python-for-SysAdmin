#!/usr/bin/env python3
# linescount-02.py

import fileinput

lines = 0
for line in fileinput.input():
	lines += 1

print('totat lines:', lines)