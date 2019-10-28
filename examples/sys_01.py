#!/usr/bin/env python3
# sys-01.py

import sys
from sys import argv

print (f'''
Python version installed: {sys.version}

Python running on platforn: {sys.platform}
''')

if len(argv) == 10:
	sys.exit('error: too many arguments')

print(f'''
argv = {argv}
len(argv) = {len(argv)}
''')

print ('Printing to stdout')
print (f'>> {sys.stderr}, "Printing to stderr"')

print(f'''
total modules search path: {len(sys.path)}
total modules loaded: {len(sys.modules)}
''')

# success
sys.exit(0)
