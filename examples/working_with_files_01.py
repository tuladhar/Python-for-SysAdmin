#!/usr/bin/env python3
# working-with-files-01.py

def main():
	try:
		with open('/etc/passwd') as f:
			for no, line in enumerate(f, 1):
				if '/bin/bash' in line:
					line = line.strip()
					print "{} {}".format(no, line)
	except IOError as e:
		print(e)

if __name__ == '__main__': main()