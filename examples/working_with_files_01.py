#!/usr/bin/env python3
# working-with-files-01.py

# NOTE : Works for Unix based systems

def main():
	try:
		with open('/etc/passwd') as f:
			for no, line in enumerate(f, 1):
				if '/bin/bash' in line: # Checks if the string /bin/bash is present in the line(each line from the file /etc/passwd). Filters out users whose default shell is Bash.
					line = line.strip()
					print ("{} {}".format(no, line))
					# Each line in /etc/passwd represents a user account, and it follows this format:
					# username:password:UID:GID:GECOS:home_directory:shell
					# password: An x or * indicates that the password is stored in the /etc/shadow file, not in this file.
					# UID: User ID. GID: Group ID. GECOS: Typically includes the user’s full name or other information.
					# home_directory: The path to the user's home directory.
					# shell: The user’s login shell (e.g., /bin/bash, /bin/sh, etc
     
	except IOError as e:
		print(e)

if __name__ == '__main__': main()