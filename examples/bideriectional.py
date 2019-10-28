#!/usr/bin/env python3
# bidirectional.py
import subprocess
from subprocess import PIPE
import sys

cmd = 'bc'
send = '1 + 1\n'

print('running command:', cmd, 'and sending input:', send)

proc = subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
stdout, stderr = proc.communicate(send)

print(f'''
exit code: {proc.poll()}

stdin:
{send}

stdout:
{stdout or None}

stderr:
{stderr or None}
''')