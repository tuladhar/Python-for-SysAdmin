#!/usr/bin/env python3
# one-way.py
import subprocess
import sys

script = sys.argv[0]

def main(argv):
	if not len(argv) == 1:
		sys.exit(f'usage: python {script} command')
	cmd = sys.argv[1]
	print ('running command:', cmd)
	proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = proc.communicate()
	print(f'''
exit code: {proc.poll()}

stdout:
{stdout or None}

stderr:
{stderr or None}
''')

if __name__ == '__main__':
	main(sys.argv[1:])
