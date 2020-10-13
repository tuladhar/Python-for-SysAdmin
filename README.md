# Python3 for Systems Administrator
[![Generic badge](https://img.shields.io/badge/Author-Puru_Tuladhar-<COLOR>.svg)](https://github.com/tuladhar)
[![Generic badge](https://img.shields.io/badge/Editor_and_Maintainer-Silent_Mobius-<COLOR>.svg)](https://github.com/silent-mobius)

## Contents
- #### Getting Started
  1. [Standard I/O](#getting-started-standard-input-output-and-error)
  2. [Working with files](#getting-started-working-with-files)
  3. [Command-line Arguments](#getting-started-command-line-arguments)
- #### Exploring Standard Modules
  1. [Operating System (OS) Module](#exploring-standard-modules-operating-system-os-module)
  2. [System-specific Module](#exploring-standard-modules-system-specific-module)
  3. [Shell Modules](#exploring-standard-modules-shell-modules)
  4. [Date and Time Modules](#exploring-standard-modules-date-and-time-modules)
  5. [Subprocess Module](#exploring-standard-modules-subprocess-module)
  6. [Argparse Module](#exploring-argparse-command-line-option-and-argument-parsing)
  6. [SQLite Module](#exploring-standard-modules-embedded-relational-database-module) ![Generic badge](https://img.shields.io/badge/Coming%20-Soon-blue)
  7. [XmlTree Module](#exploring-xmltree-module) ![Generic badge](https://img.shields.io/badge/Coming%20-Soon-blue)
  8. [JSON Module]( #exploring-json-module-exploring-json-module)
  9. [Regular Expressions Module](#exprloting-standard-regular-expression-module) ![Generic badge](https://img.shields.io/badge/Coming%20-Soon-blue)
  10. [Compression Module](#exploring-compression-module) ![Generic badge](https://img.shields.io/badge/Coming%20-Soon-blue)
  11. [Platform Module](#exploring-platform-module) ![Generic badge](https://img.shields.io/badge/Coming%20-Soon-blue)
  12. [Signal Module](#exploring-standard-modules-signal-module) ![Generic badge](https://img.shields.io/badge/Coming%20-Soon-blue)
  13. [Socket Module](#exploring-standard-modules-socket-module) ![Generic badge](https://img.shields.io/badge/Coming%20-Soon-blue)

- #### Exploring External Modules
  -  #### Network Modules
  1. [Netmiko Module](#exploring-standard-modules-netmiko-module) ![Generic badge](https://img.shields.io/badge/Coming%20-Soon-blue)
  2. [Twisted Module](#exploring-standard-modules-twisted-module) ![Generic badge](https://img.shields.io/badge/Coming%20-Soon-blue)
  3. [Ipaddress Module](#exploring-standard-modules-ipaddress-module) ![Generic badge](https://img.shields.io/badge/Coming%20-Soon-blue)
  4. [Netsnmp Module](#exploring-standard-modules-netsnmp-module) ![Generic badge](https://img.shields.io/badge/Coming%20-Soon-blue)
  - #### DB Modules
  1. [SQLAlchemy Module](#exploring-standard-modules-sqlalchemy-module) ![Generic badge](https://img.shields.io/badge/Coming%20-Soon-blue)

---

## `Getting Started` Standard Input, Output and Error

Standard input, output and error (commonly referred to as `stdin`, `stdout` and `stderr`) are what's called pipes.

These pipes are normally connected to the terminal window where you are working.

When printing something (using `print()`), it goes to the `stdout` pipe by default; when your program needs to print errors (like a traceback in Python), it goes to the `stderr` pipe; and when your program requires input from a user or other programs, it goes to the `stdin` pipe.

```bash
$ cat /etc/passwd | grep /bin/bash
#  `\_ writes to stdout        `\_ reads from stdin

$ ls no_such_file.txt
#  `\_ writes to stderr
```

Python built-in `sys` module provides `stdin`, `stdout` and `stderr` as a file-objects, exposing `read()`, `readlines()`, `write()`, `writelines()` methods, as shown below:

```python
#!/usr/bin/env python3
import sys

# writing to stdout pipe
print ('Hello, world')
sys.stdout.write('Hello, world\n')

# writing to stderr pipe
print("Error occured")
sys.stderr.write("Error occured\n")

# reading single line from stdin pipe
sys.stdout.write('Username: ')
username  = sys.stdin.readline()
print (username)

# reading 'n' number of characters from stdin
print ('Enter few characters and press Ctrl-D')
data = sys.stdin.read(1024)
print('len(data):', len(data))

# reading lines (separated by newlines) from stdin
print('Enter few lines and press Ctrl-D')
lines = sys.stdin.readlines()
print ('total lines read:', len(lines))
```

---

## `Getting Started` Working with files

Python built-in `open` function is the standard interface for working with files. `open` returns a file object with familiar methods for performing read/write operations.

```
open(file, mode='r')
```

###### Common arguments:

- __file:__ absolute or relative path of the file. e.g: `/etc/passwd`, `./ip-list.txt`
- __mode:__ an optional string specifying mode in which the file is opened. Default's to `r` for reading in text mode. Common values are:
 - `w` write only *(truncates the file already exists)*
 - `x` create and write to a new file _(if file already exists then open fails)_
 - `a` append to a file *(insert data to end of the file)*
 - `+` updating a file (reading and writing). e.g: `r+` `w+`
 - `b` binary mode for non-text files. Contents are returned as `byte` objects.
 - `t` text mode (default). Contents are returned as `strings`.

###### File object methods:

- `.close()`
- `.read(size=-1)` read at most `n` characters. If `n` is negative or ommited, reads the whole file until `EOF`.
- `.readline()` Read single line until newline or `EOF`.
- `.readlines()` Read all newlines and returns as a list.
- `.write(data)` Write data to file. Returns number of characters written.
- `.writelines(list)` Write all data in the list. Useful for writing multiple lines to a file.

##### Example

```python
## Reading a file
r = open('/etc/passwd')
# same as:
# r = open('/etc/passwd', 'r')
passwd = r.readlines()
for line in passwd:
	line = line.strip()
	size = len(line)
	print(size, line)
r.close()

## Reading a file using `with` statement, automatically closes the file
with open('/etc/passwd') as f:
	pass

## Writing to a file
w = open('test.txt', 'w')
w.write('127.0.0.1\n')
w.flush()
lines = ['1.1.1.1\n', '2.2.2.2\n', '3.3.3.3\n']
w.writelines(lines)
w.close()
```
---
### Handling Errors

All `open` related errors raises `IOError` exception.

```python
try:
	f = open('/etc/passwd')
except IOError as e:
	print ('Opps, something went wrong.')
	print (e)
```
---

#### Reading `/etc/passwd` and search each line for `/bin/bash` shell; when found print the line number and the line

```python
#!/usr/bin/env python3
# working-with-files-01.py

def main():
	try:
		with open('/etc/passwd') as f:
			for no, line in enumerate(f, 1):
				if '/bin/bash' in line:
					line = line.strip()
					print(f'{no} {line}')
	except IOError as e:
		print(e)

if __name__ == '__main__': main()
```

---

#### Using `fileinput` High-level module

`fileinput` module allows to quickly write a loop over standard input or a list of files.

##### Example

```python
#!/usr/bin/env python3
# linescount-02.py

import fileinput

lines = 0
for line in fileinput.input():
	lines += 1

print('totat lines:', lines)
```

```bash
$ cat /etc/passwd | python3 linescount.py
totat lines: 86
$ python3 linescount.py /etc/services
totat lines: 13921
$ python3 linescount.py /etc/services /etc/passwd /etc/hosts
totat lines: 14023
```

By default, `fileinput.input()` will read all lines from files given as an argument to the script; if no arguments given then defaults to standard input.

---

## `Getting Started` Command-line Arguments

`sys` module provides `argv` variable containing the list of arguments passed to the script when executed as a command-line application.

>NOTE: The first argument `sys.argv[0]` is always the name of the script itself.

```python
#!/usr/bin/env python3
# argv_01.py

import sys

print ('sys.argv:', sys.argv)
print ('length:', len(argv))
```
```bash
$ python3 args_01.py --help
['argv-01.py', '--help']
2
$ python3 args_01.py 1 2 3
['argv-01.py', '1', '2', '3']
4
```

#### Accept specific number of arguments and fail if not satistified.

```python
#!/usr/bin/env python3
# args-02.py
import sys

# NOTE: [1:] excludes the first item at index 0, i.e script name
argv_len = len(sys.argv[1:])

if not argv_len == 2:
	sys.exit(f'invalid number of arguments (expected 2, given: {argv_len})')

print('two arguments are:', sys.argv[1:])
```

```bash
$ python args_02.py
invalid number of arguments (expected 2, given: 0)
$ python args_02.py 1
invalid number of arguments (expected 2, given: 1)
$ python args_02.py 1 2  
two arguments are: ['1', '2']
$ python args_02.py 1 2 3
invalid number of arguments (expected 2, given: 3)
```

#### Simple Implementation of `grep' command

```python
#!/usr/bin/env python3
# grep.py

import sys

script = sys.argv[0]

def print_usage():
	sys.exit(f'Usage: python {script} pattern')

def main(argv):
	if not len(argv) == 1:
		print_usage()

	pattern = argv[0]

	for line in sys.stdin:
		if pattern in line:
			print(line.strip())

if __name__ == '__main__':
	main(sys.argv[1:])
```

```bash
$ cat /etc/services | python3 grep.py 8080
http-alt	8080/udp     # HTTP Alternate (see port 80)
http-alt	8080/tcp     # HTTP Alternate (see port 80)
```

---

#### Improvement Exercises
- Extend `grep.py` to read from a file instead of standard input, and can be run as:

```bash
$ python3 grep.py 8080 /etc/services
```

- Extend `grep.py` to read from a file if given as a second argument or default back to read from standard input similar to what `grep` does.

```bash
$ cat /etc/services | python3 grep.py 8080
# and also should works as
$ python3 grep.py 8080 /etc/services
```

---

## `Exploring Standard Modules` Operating System (OS) Module

Python built-in `os` module exposes operating system dependent functionality in a portable way, thus works across many different platforms.

```
import os
```

###### Working with environmental variables:

- `os.environ` a dictionary mapping system environment variables. e.g. `os.environ.get('SHELL')`
- `os.getenv(key)` retrieve a specific variable.
- `os.putenv(key, value)`. change variable to specific value. e.g. `os.putenv('HOME', '/opt')`

###### Working with files and directories:

- `os.tmpnam` returns a unique file name that can be used to create temporariry file. `mktemp()` from `tempfile` module is more secure.
- `os.mkdir(path)` `os.rmdir(path)` `os.chdir(path)` `os.listdir(path)`
- `os.getcwd()` returns current working directory as string. Similar to `pwd` command.
- `os.stat(path)` similar to `stat` command
- `os.walk(path)` recursively walk the dictionary tree, similar to `ls -R`. Returns generator yielding 3-tuple `(dirpath, dirnames, files)`

##### Example

```bash
>>> import os

# environment variables
>>> os.environ['SHELL'] # or os.environ.get('SHELL') or os.getenv('SHELL')
'bash'

# Get a temporary filename using `tempfile` module
>>> from tempfile import mktemp
>>> temp = mktemp()
'/var/folders/6s/4xn2fv852_1ghssypng0wwfw0000gn/T/tmp15O9aR'

# Create the temporary file and write 'test'
>>> with open(temp, 'w') as f:
... 	f.write('test\n')

# Get the file stat, such as creation timestamp (ctime)
>>> st = os.stat(temp)
>>> st.st_ctime
1436466688.0

# convert timestamp to human readable format, we'll cover date & time later.
>>> import datetime
>>> d = datetime.datetime.fromtimestamp(st.st_ctime)
>>> d.year # d.month, d.hour and so on...
2016
```
--
###### Working with Path names  `os.path`:

- `os.path.abspath(path)` get absolute path.
- `os.path.basename(path)` get the filename excluding the directory part. Opposite of  `os.path.dirname` which excludes filename part and returns directory path.
- `os.path.exists(path)` returns `True` if path exists else `False`.
- `os.path.getsize(path)` return size (in bytes) for a given path.
- `os.path.isfile(path)`, `os.path.isdir(path)` returns `True` or `False` if path is file or a directory.
- `os.path.getctime(path)`,  `os.path.getmtime(path)` Similar to `os.stat(path).ctime`, `os.stat(path).mtime()`

#### Learn more at [os.path documentation](https://docs.python.org/3.7/library/os.path.html)

##### Example

```bash
>>> os.path.isdir('/etc')
True

>>> os.chdir('/etc')

>>> os.getcwd()
'/etc'

>>> os.path.abspath('hosts')
'/etc/hosts'

>>> os.path.isfile('/etc/hosts')
True

>>> os.path.getsize('/etc/hosts')
475

>>> print (os.path.basename('/etc/passwd'))
'passwd'

>>> print (os.path.dirname('/etc/passwd'))
'/etc'
```


###### Process related functions:

- `os.getpid()` get id of current process and `os.getppid()`to get parent process id.
- `os.system(command)` execute a command and returns exit code.

###### Getting System Informations:

- `os.uname()` returns a 5-tuple `(sysname, nodename, release, version, machine)` identifying the current OS. Similar to `uname -a` command.
- `os.getloadavg()` returns 3-tuple containing 1-min, 5-min and 15-min load average.

--

#### Print size (in bytes) of all files in a given directory

```python
#!/usr/bin/env python3
# filesizes.py

import os
import sys

script = sys.argv[0]

def print_usage():
	print(f' >> {sys.stderr}, "Usage: python3 {script} DIR"')
	sys.exit(1)

def filesizes(path):
	''' calculate and print size of each file in a given directory. '''

	for dirpath, dirnames, filenames in os.walk(path):
		for filename in filenames:
			filepath = os.path.join(dirpath, filename)
			_bytes = os.path.getsize(filepath)
			print (f'{_bytes}, {filepath}')

def main(argv):
	if not len(argv) == 1:
		print_usage()

	path = argv[0]
	filesizes(path)

if __name__ == '__main__':
	main(sys.argv[1:])

```

>```bash
	$ python3 filesizes.py .
	678 ./filesizes.py
	```

#### [Learn more about OS module](https://docs.python.org/3.7/library/os.html)

---
## `Exploring Standard Modules` System-specific Module

Python built-in `sys` module exposes system-specific parameters and functions. This module provides access to some variables used or maintained by the interpreter and functions that interact strongly with the interpreter. `sys` module is always available.

```
import sys
```



###### Commonly used variables and functions:

- `sys.argv` contains list of command-line arguments. *Already covered.*
- `sys.exit([arg])` exit the program. `arg` is optional, can be `0` to indicate success, `> 0` for failure or `string` to display the errors during exit.
- `sys.version` stores version of Python installed.
- `sys.stdin` `sys.stdout` `sys.stderr` File objects corresponding to the interpreter's standard input, output and error pipes.
- `sys.platform` stored the name of the platofrm Python is running. Such as `darwin` for MacOS, `linux` for Linux and others
- `sys.path` A list of strings that specified the search path while importing modules via `import` statement.
- `sys.modules` A dictionary mapping the `{ 'module_name': 'module_path', ... }` which have already been loaded.

---

```python
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
```

###### Output should look like this

```bash
$ python3 sys-01.py

Python version installed: 3.7.4 (default, Jul  9 2019, 16:48:28)
[GCC 8.3.1 20190223 (Red Hat 8.3.1-2)]

Python running on platforn: linux


argv = ['sys_01.py']
len(argv) = 1

Printing to stdout
>> <_io.TextIOWrapper name='<stderr>' mode='w' encoding='UTF-8'>, "Printing to stderr"

total modules search path: 7
total modules loaded: 57


$ echo $?
0
```

#### [Learn more about sys module](https://docs.python.org/3.7/library/sys.html)

---

## `Exploring Standard Modules` Shell Modules

### shutil module — High-level file operations

The `shutil` module provides high-level operations on files or collection of files.

###### Copy Operations:

- `shutil.copy(src, dst)` Copy src file to dst file or directory.
- `shutil.copymode(src, dst)` Copy permission mode of src  file to dst file.
- `shutil.copystat(src, dst)` Copy permission mode, modification and creation date from src file to dst file.
- `shutil.copy2(src, dst)` Similar to `cp -p` command or equivalent of `shutil.copy` and `shutil.copystat`.

###### Move Operations:

- `shutil.move(src, dst)` Move src file to dst file or directory.

#### [Learn more about shutil module](https://docs.python.org/3.7/library/shutil.html)

---

### glob module — Unix style pathname pattern expansion

The `glob` module finds all the pathnames matching a specified pattern according to the rules used by the Unix shell.

- `glob.glob(pattern)` Return a list of path names that match the path pattern. Path can be absolute `/usr/local/bin/*.py` or relative `local/bin/*.py`.

##### Example

```bash
>>> import glob
>>> glob.glob('/etc/sysconfig/network-scripts/ifcfg*')
['/etc/sysconfig/network-scripts/ifcfg-venet0',
 '/etc/sysconfig/network-scripts/ifcfg-lo']

>>> glob.glob('/etc/*.conf')
['/etc/vnstat.conf',
 '/etc/sudo.conf',
 '/etc/resolv.conf',
 '/etc/host.conf',
 '/etc/logrotate.conf']
```

#### [Learn more about glob module](https://docs.python.org/3.7/library/glob.html)

---

## `Exploring Standard Modules` Date and Time Modules

### time module — Clock time

The `time` module exposes the time-related functions from the underlying C library.

###### Commonly used functions:

- `time.time()` returns the number of seconds since the start of the epoch as a floating-point value.
- `time.ctime()` returns a human-friendly date and time representation.
- `time.gmtime()` returns an object containing current time in UTC format.
- `time.localtime()` returns an object containing the current time in current time zone.
- `time.tzset()` sets the time zone based on `TZ` environment variable: `os.environ.get('TZ')`

##### Example

```bash
>>> import time
>>> time.time()
1459924583.396017

>>> # current time in UTC
>>> utc = time.gmtime()
>>> dir(utc)
['tm_hour',
 'tm_isdst',
 'tm_mday',
 'tm_min',
 'tm_mon',
 'tm_sec',
 'tm_wday',
 'tm_yday',
 'tm_year']

>>> # current time in GMT by updating timezone
>>> import os
>>> os.putenv('TZ', 'GMT') # or os.environ['TZ'] = 'GMT'
>>> time.tzset()
>>> gmt = '{} {}'.format(time.ctime(), time.tzname[0])
```

#### [Learn more about time module](https://docs.python.org/3.7/library/time.html)

---

## datetime module — Date and Time Value Manipulation

The `datetime` module includes functions and classes for doing date and time parsing, formatting, and arithmetic.

##### Commonly used functions:

- `datetime.date.today()` returns current date object without the time
- `datetime.datetime.today()` returns current date and time object
- `datetime.datetime.fromtimestamp(float)` convert unix timestamp to datetime object
- `datetime.timedelta` future and past dates can be calculated using basic arithmetic (+, -) on two datetime objects, or by combining a datetime with a timedelta object.

##### Example

```python
>>> import datetime
>>> today_date = datetime.date.today()
>>> ten_days = datetime.timedelta(days=10)
>>> today_date - ten_days # past
>>> today_date + ten_days # future
```

###### Alternate formats can be generated using `strftime()` and `strptime` to convert formatted string to `datetime` object.

```bash
>>> import datetime

# convert datetime to custom format
>>>  format = "%a %b %d %H:%M:%S %Y"
>>> today = datetime.datetime.today()
>>> today.strftime(format)
'Mon Oct 14 17:56:24 2019'

# convert formatted string to datetime object
>>> datetime.datetime.strptime('Mon Oct 14 17:56:24 2019', format)
datetime.datetime(2019, 10, 14, 17, 56, 24)
```

#### [Learn more about datetime module](https://docs.python.org/3.7/library/datetime.html)

---

## `Exploring Standard Modules` Subprocess Module

### subprocess module — Subprocess management

The `subprocess` module allows to run new processes, connect to their input/output/error pipes, and obtain their return codes.

The module defines a many helper functions and a class called `Popen` which allows to set up the new process so the parent can communicate with it via pipes.


### Running external commands

To run an external command without interacting with, use `subprocess.call(command, shell=True)` function.

```python
>>> import subprocess
>>> rc = subprocess.call('ls -l /etc', shell=True)
0
>>> rc = subprocess.call('ls -l no_such_file.txt', shell=True)
1
```

Setting the **shell** argument to a **True** value causes subprocess to spawn a shell process (normally bash), which then runs the command. Using a shell means that variables, glob patterns, and other special shell features in the command string are processed before the command is run.

```py
>>> import subprocess
>>> subprocess.call('echo $PATH' )

# will return error
subprocess.call('echo $PATH', shell=True)
# will print the shell PATH variable value
```

--

### Error Handling

The return value from `subprocess.call()` is the exit code of the program and is used to detect errors. The `subprocess.check_call()` function works like `call()`, except that the exit code is checked, and if it returns non-zero, then a `subprocess.CalledProcessError` exception is raised.

```python
#!/usr/bin/env python3
# check_call.py

import sys
import subprocess

try:
	cmd = 'false'
	print ('running command:',cmd)
	subprocess.check_call(cmd, shell=True)
except subprocess.CalledProcessError as error:
	sys.exit(f'error: {error}')
```

```bash
$ python3 check_call.py
running command: false
error: Command 'false' returned non-zero exit status 1
```

---

### Capturing Command Output

To run an external command and capture it's output, use `check_output(command, shell=True)` to capture the output for later processing. If command returns non-zero, then a `CalledProcessError` exception is raised similar to `check_call`.

>Execute `cat /etc/hosts` and write the output to a file `hosts.txt`

```python
#!/usr/bin/env python3
# capture_output.py

import subprocess
import sys

try:
	cmd = 'cat /etc/hosts'
	print('running command:', cmd)
	output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError as error:
	sys.exit('error: {error}')
else:
	print('success!')
	with open('hosts.txt', 'w') as f:
		f.write(output)
		#this should give an error in python3.6+
```

By default, `check_output` captures outputs written to `stdout`. Setting the `stderr=subprocess.STDOUT` causes `stderr` outputs to redirected to `stdout`, so errors can be captured as well.

---

### Working directory with Popen

The `call()`, `check_call()`, and `check_output()` are wrappers around the `Popen` class. Using `Popen` directly gives more control over how the command is run and how its input and output streams are processed.

#### One-Way Communication with a Process

To run a process and capture it's output, set the `stdout` and `stderr` arguments to `subprocess.PIPE` and call `communicate()`.

`communicate()` returns 2-tuple `(stderr_output, stderr_putput)`

```python
#!/usr/bin/env python3
# one-way.py
import subprocess
import sys

script = sys.argv[0]

def main(argv):
	if not len(argv) == 1:
		sys.exit(f'usage: python3 {script} command')
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
```

```bash
$ python3 one_way.py ls
running command: ls

exit code: 0

stdout:
b'capture_output.py\ncheck_call.py\nhosts.txt\none_way.py\nsys_01.py\n'

stderr:
None

```

---

### Bidirectional Communication with a Process

To set up the Popen instance for reading and writing at the same time, pass additional argument `stdin=subprocess.PIPE`.

```python
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
```

```bash
$ python3 bidirectional.py
running command: bc and sending input: 1 + 1

exit code: 0

stdin:
1 + 1

stdout:
2

stderr:
None
```

#### [Learn more about subprocess module](https://docs.python.org/3.7/library/subprocess.html?highlight=subprocess#module-subprocess)

## `Exploring Argparse` Command-Line Option and Argument Parsing

Python built-in `argparse` is parser for command-line options, arguments and subcommands. The argparse module provides argument management just like `sys.argv`, but with options, e.g it generates help and usage messages and issues errors when users give the program invalid arguments.
Let’s show the sort of functionality by making use of the ls command:

```bash
$ ls
examples  LICENSE  README.md
$ ls -l
total 44
drwxrwxr-x.  4 que que  4096 Oct 14 18:05 .
drwxrwxr-x. 24 que que  4096 Oct 13 15:32 ..
drwxrwxr-x.  2 que que  4096 Oct 14 18:48 examples
drwxrwxr-x.  8 que que  4096 Oct 15 01:01 .git
-rw-rw-r--.  1 que que  1210 Oct 13 15:32 LICENSE
-rw-rw-r--.  1 que que 24357 Oct 15 01:02 README.md
$ ls --help
Usage: ls [OPTION]... [FILE]...
List information about the FILEs (the current directory by default).
Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.
...
```

A few concepts we can learn from the four commands:

- When you run the "ls -l" command with options, it will default displaying the contents of the current directory
- The "-l" is knowns as an "optional argument"
- If you want to display the help text of the ls command, you would type "ls --help"

To start using the argparse module, we first have to import it.

```py
>>> import argparse
```

#### Intro to positional arguments

 The following code is a Python program that takes a list of integers and produces either the sum or the max:

##### Example

```py
#!/usr/bin/env python3
#app.py
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                   help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                   const=sum, default=max,
                   help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))
```

Assuming the Python code above is saved into a file called `app.py`, it can be run at the command line and provides useful help messages

```bash
$ app.py -h
usage: prog.py [-h] [--sum] N [N ...]

Process some integers.

positional arguments:
 N           an integer for the accumulator

optional arguments:
 -h, --help  show this help message and exit
 --sum       sum the integers (default: find the max)

$ app.py 1 2 3 4
4

$ app.py 1 2 3 4 --sum
10
```

### Creating a parser

The first step in using the `argparse` is creating an `ArgumentParser` object:

```py
>>> parser = argparse.ArgumentParser(description='Process some integers.')
```

The `ArgumentParser` object will hold all the information necessary to parse the command line into python data types.

### Adding arguments

Filling an`ArgumentParser` with information about program arguments is done by making calls to the `ArgumentParser.add_argument` method. Generally, these calls tell the `ArgumentParser` how to take the strings on the command line and turn them into objects. This information is stored and used when `ArgumentParser.parse_args` is called. For example:

```py
>>> parser.add_argument('integers', metavar='N', type=int, nargs='+',
...                     help='an integer for the accumulator')
>>> parser.add_argument('--sum', dest='accumulate', action='store_const',
...                     const=sum, default=max,
...                     help='sum the integers (default: find the max)')
```

Later, calling `parse_args` will return an object with two attributes, integers and accumulate. The integers attribute will be a list of one or more ints, and the accumulate attribute will be either the `sum` function, if --sum was specified at the command line, or the `max` function if it was not.

### Parsing arguments

`ArgumentParser` parses args through the `ArgumentParser.parse_args` method. This will inspect the command-line, convert each arg to the appropriate type and then invoke the appropriate action. In most cases, this means a simple namespace object will be built up from attributes parsed out of the command-line:

```py
>>> parser.parse_args(['--sum', '7', '-1', '42'])
Namespace(accumulate=<built-in function sum>, integers=[7, -1, 42])
```

In a script,`ArgumentParser.parse_args` will typically be called with no arguments, and the `ArgumentParser` will automatically determine the command-line args from `sys.argv`.

### ArgumentParser objects

Create a new `ArgumentParser` object. Each parameter has its own more detailed description below, but in short they are:

- `description` - Text to display before the argument help.
- `epilog` - Text to display after the argument help.
- `add_help` - Add a -h/--help option to the parser. (default: True)
- `argument_default` - Set the global default value for arguments. (default: None)
- `parents` - A list of `ArgumentParser` objects whose arguments should also be included.
- `prefix_chars` - The set of characters that prefix optional arguments. (default: '-')
- `fromfile_prefix_chars` - The set of characters that prefix files from which additional arguments should be read. (default: None)
- `formatter_class` - A class for customizing the help output.
- `conflict_handler` - Usually unnecessary, defines strategy for resolving conflicting optionals.
- `prog` - The name of the program (default:`sys.argv[0]`)
- `usage` - The string describing the program usage (default: generated)

#### [Learn more about argparse module](https://docs.python.org/3.7/library/argparse.html)

## `Exploring SQLite Module` exploring-standard-modules-embedded-relational-database-module

SQLite is a C-language library that implements a SQL like database engine which is relatively quick, serverless and self-contained, high-reliable. SQLite comes built-in with most of the moden software, hardware devices and browsers, thus Python also has embedded SQLite engine named sqlite3.

To Start using the sqlite3 library:

```py
>>> import sqlite3
```

#### Commonly used functions:

- `sqlite3.connect()` - A connection object is created using the connect() function e.g **connection = sqlite.connect('name_of_file_db.db')**
- `connection.cursor()` - To execute SQLite statements, cursor object is needed. You can create it using the cursor() method. e.g **cursor_object = connection.cursor()**
- `connection.execute()` - To create a table in SQLite3, you can use the Create Table, Insert Into Table, Update Table, or Select query with the execute() method of SQLite library. For example **cursor_object.execute("CREATE TABLE employees()"); connection.commit()**
- `connection.commit()` - The commit() method saves all the changes we make.
- `cursor_object.fetchall()` -  To fetch the data from a database we will execute the SELECT statement and then will use the fetchall() method of the cursor object to store the values into a variable, e.g  **cursor_object.execute('SELECT * FROM employees') ; rows = cursor_object.fetchall()**
- `cursor_object.rowcount()` - The SQLite3 rowcount is used to return the number of rows that are affected or selected by the latest executed SQL query
- `cursor_object.executemany()` - It can use the **executemany** statement to insert multiple rows at once.
- `connection.close()` - You are done with your database, it is a good practice to close the connection with close() method. e.g. **connection.close()**

#### [Learn More about SQLite3 Module](https://docs.python.org/3.7/library/sqlite3.html)

## `Exploring XmlTree Module` exploring-xmltree-module


#### [Learn More about XmlTree Module](https://docs.python.org/3.7/library/xml.etree.elementtree.html#module-xml.etree.ElementTree)




## `Exploring JSON Module` exploring-json-module

JSON is text, written with JavaScript object notation. JSON is a syntax for storing and exchanging data.
It is commonly used for transmitting data in web applications (e.g., sending some data from the server to the client, so it can be displayed on a web page
and vice versa

- `json.loads()`
- take a file object and returns the json object. A JSON object contains data in the form of key/value pair. The keys are strings and the values are the JSON types

- `json.dumps()`
-json.dumps() function converts a Python object into a json string
.It is the exact opposite of json.loads.

THIS IS THE ENCODING DECODING LIST

 JSON -Python 
 
 1)object- DICT   
 2)array - list  
 3)string - str   
 4)int  -  int  
 5)real  -  float 
 6)true  -  true  
 7)False - False 
 8)NULL  - NONE  




 - `  Encoding is from python to JSON(final type)`
>>> json.JSONEncoder().encode({"foo": ["bar", "baz"]})
'{"foo": ["bar", "baz"]}'


- `Decoding is from JSON to python(final type)`

## Encoding functions

- `iterencode(o)`
-Encode the given object, o, and yield each string representation as available. For example:
>>>for chunk in json.JSONEncoder().iterencode(bigobject):
    mysocket.write(chunk)]
    
` -sort-keys` -Sort the output of dictionaries alphabetically by key.

`-h, --help¶`- help box 

`infile`-to check your Json file for syntax

`outfile`-Write the output of the infile to the given outfile

## Note
If the optional infile and outfile arguments are not specified, sys.stdin and sys.stdout will be used respectively:

 `json.tool `- to validate and pretty-print JSON objects.
 
 `raw_decode`- This can be used to decode a JSON document from a string that may have extraneous data at the end.

#### [Learn More about JSON Module](https://docs.python.org/3.7/library/json.html)
