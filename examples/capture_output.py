#!/usr/bin/env python3
# capture_output.py

import subprocess
import sys

try:
	cmd = 'cat /etc/hosts'
	print('running command:', cmd)
	output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError as error:
	sys.exit(f'error: {error}')
else:
	print('success!')
	with open('hosts.txt', 'w') as f:
		f.write(str(output))
