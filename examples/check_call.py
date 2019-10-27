#!/usr/bin/env python3
# check_call.py

import sys
import subprocess

try:
	cmd = 'false'
	print ('running command:',cmd)
	subprocess.check_call(cmd, shell=True)
except subprocess.CalledProcessError as error:
	sys.exit('error: {}'.format(error))
