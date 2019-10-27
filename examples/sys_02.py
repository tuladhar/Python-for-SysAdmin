#!/usr/bin/env python3
# args-02.py
import sys

# NOTE: [1:] excludes the first item at index 0, i.e script name
argv_len = len(sys.argv[1:])

if not argv_len == 2:
	sys.exit('invalid number of arguments (expected 2, given: {})'.format(argv_len))

print('two arguments are:', sys.argv[1:])