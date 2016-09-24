#Python for Systems Administrator - Part I
### Author: [Puru Tuladhar] (github.com/tuladhar)

>##Contents

>1. **Getting Started**
  1. [Standard I/O](https://github.com/tuladhar/Python-for-SysAdmin-Part-I/blob/master/README.md#getting-started-standard-input-output-and-error)
  2. [Working with files](https://github.com/tuladhar/Python-for-SysAdmin-Part-I/blob/master/README.md#getting-started-working-with-files)
  3. [Command-line Arguments](https://github.com/tuladhar/Python-for-SysAdmin-Part-I/blob/master/README.md#getting-started-command-line-arguments)

>2. **Exploring Standard Modules**
  1. [Operating System (OS) Module](https://github.com/tuladhar/Python-for-SysAdmin-Part-I/blob/master/README.md#exploring-standard-modules-operating-system-os-module)
  2. [System-specific Module](https://github.com/tuladhar/Python-for-SysAdmin-Part-I/blob/master/README.md#exploring-standard-modules-system-specific-module)
  3. [Shell Modules](https://github.com/tuladhar/Python-for-SysAdmin-Part-I/blob/master/README.md#exploring-standard-modules-shell-modules)
  4. [Date and Time Modules](https://github.com/tuladhar/Python-for-SysAdmin-Part-I/blob/master/README.md#exploring-standard-modules-date-and-time-modules)
  5. [Subprocess Module](https://github.com/tuladhar/Python-for-SysAdmin-Part-I/blob/master/README.md#exploring-standard-modules-subprocess-module)

---
## `Getting Started` Standard Input, Output and Error

Standard input, output and error (commonly referred as `stdin`, `stdout` and `stderr`) are what's called pipes.

These pipes are normally connected to the terminal window where you are working.

When printing something (using `print`), it goes to the `stdout` pipe by default; when your program needs to print errors (like a traceback in Python), it goes to the `stderr` pipe; and when your program requires input from a user or other programs, it is goes to the `stdin` pipe.

```bash
$ cat /etc/passwd | grep /bin/bash
#  `\_ writes to stdout        `\_ reads from stdin

$ ls no_such_file.txt
#  `\_ writes to stderr
```

Python built-in `sys` module provides `stdin`, `stdout` and `stderr` as a file-objects, exposing `read()`, `readlines()`, `write()`, `writelines()` methods, as shown below:

```python
import sys

# writing to stdout pipe
print 'Hello, world'
sys.stdout.write('Hello, world\n')

# writing to stderr pipe
print >> sys.stderr, 'Error occured'

# reading single line from stdin pipe
sys.stdout.write('Username: ')
username  = sys.stdin.readline()
print username

# reading 'n' number of characters from stdin
print 'Enter few characters and press Ctrl-D'
data = sys.stdin.read(1024)
print 'len(data):', len(data)

# reading lines (separated by newlines) from stdin 
print 'Enter few lines and press Ctrl-D'
lines = sys.stdin.readlines()
print 'total lines read:', len(lines)
```

---
## `Getting Started` Working with files

Python built-in `open` function is the standard interface for working with files. `open` returns a file object with familiar methods for performing read/write operations.

```
open(file, mode='r')
``` 

######Common arguments:

- __file:__ absolute or relative path of the file. e.g: `/etc/passwd`, `./ip-list.txt`
- __mode:__ an optional string specifying mode in which the file is opened. Default's to `r` for reading in text mode. Common values are:
 - `w` write only *(truncates the file already exists)*
 - `x` create and write to a new file _(if file already exists then open fails)_
 - `a` append to a file *(insert data to end of the file)*
 - `+` updating a file (reading and writing). e.g: `r+` `w+`
 - `b` binary mode for non-text files. Contents are returned as `byte` objects.
 - `t` text mode (default). Contents are returned as `strings`.

######File object methods:

- `.close()`
- `.read(size=-1)` read at most `n` characters. If `n` is negative or ommited, reads the whole file until `EOF`.
- `.readline()` Read single line until newline or `EOF`.
- `.readlines()` Read all newlines and returns as a list.
- `.write(data)` Write data to file. Returns number of characters written.
- `.writelines(list)` Write all data in the list. Useful for writing multiple lines to a file.

>###### Example

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
--
### Handling Errors

All `open` related errors raises `IOError` exception.

```python
try:
	f = open('/etc/passwd')
except IOError as e:
	print 'Opps, something went wrong.'
	print e
```
--

#### Reading `/etc/passwd` and search each line for `/bin/bash` shell; when found print the line number and the line

```python
#!/usr/bin/python
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
```
--
#### Using `fileinput` High-level module

`fileinput` module allows to quickly write a loop over standard input or a list of files.

> ###### Example

```python
#!/usr/bin/python
# linescount-02.py

import fileinput

lines = 0
for line in fileinput.input():
	lines += 1

print 'totat lines:', lines
```

>```bash
$ cat /etc/passwd | python linescount.py          
totat lines: 86
$ python linescount.py /etc/services 
totat lines: 13921
$ python linescount.py /etc/services /etc/passwd /etc/hosts
totat lines: 14023
```

By default, `fileinput.input()` will read all lines from files given as an argument to the script; if no arguments given then defaults to standard input.

---
## `Getting Started` Command-line Arguments

`sys` module provides `argv` variable containing the list of arguments passed to the script when executed as a command-line application.

>NOTE: The first argument `sys.argv[0]` is always the name of the script itself. 

```python
#!/usr/bin/python
# argv_01.py

import sys

print 'sys.argv:', sys.argv
print 'length:', len(argv)
```
>```bash
$ python args_01.py --help
['argv-01.py', '--help']
2 
$ python args_01.py 1 2 3
['argv-01.py', '1', '2', '3']
4
```

#### Accept specific number of arguments and fail if not satistified.

```python
# args-02.py
import sys

# NOTE: [1:] excludes the first item at index 0, i.e script name
argv_len = len(sys.argv[1:])

if not argv_len == 2:
	sys.exit('invalid number of arguments (expected 2, given: {})'.format(argv_len))

print 'two arguments are:', sys.argv[1:] 
```
>```bash
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
#!/usr/bin/python
# grep.py

import sys

script = sys.argv[0]

def print_usage():
	sys.exit('Usage: python {} pattern'.format(script))

def main(argv):
	if not len(argv) == 1:
		print_usage()
	
	pattern = argv[0]
	
	for line in sys.stdin:
		if pattern in line:
			print line.strip()

if __name__ == '__main__':
	main(sys.argv[1:])
```

>```bash
$ cat /etc/services | python grep.py 8080
http-alt	8080/udp     # HTTP Alternate (see port 80)
http-alt	8080/tcp     # HTTP Alternate (see port 80)
```

--

#### Improvement Exercises
- Extend `grep.py` to read from a file instead of standard input, and can be run as:

```bash
$ python grep.py 8080 /etc/services
```

- Extend `grep.py` to read from a file if given as a second argument or default back to read from standard input similar to what `grep` does.

```bash
$ cat /etc/services | python grep.py 8080
# and also should works as
$ python grep.py 8080 /etc/services
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

>###### Example

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
- Learn more at [os.path documentation](https://docs.python.org/2.7/library/os.path.html)

> ###### Example

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

>>> print os.path.basename('/etc/passwd')
'passwd'

>>> print os.path.dirname('/etc/passwd')
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
#!/usr/bin/python
# filesizes.py

import os
import sys

script = sys.argv[0]

def print_usage():
	print >> sys.stderr, 'Usage: python {} DIR'.format(script)
	sys.exit(1)

def filesizes(path):
	''' calculate and print size of each file in a given directory. '''
	
	for dirpath, dirnames, filenames in os.walk(path):
		for filename in filenames:
			filepath = os.path.join(dirpath, filename)
			bytes = os.path.getsize(filepath)
			print '{} {}'.format(bytes, filepath)

def main(argv):
	if not len(argv) == 1:
		print_usage()
	
	path = argv[0]
	filesizes(path)

if __name__ == '__main__':
	main(sys.argv[1:])

```

>```bash
$ python filesizes.py . 
678 ./filesizes.py 
```

#### [Learn more about OS module](https://docs.python.org/2.7/library/os.html)

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

--

```python
#!/usr/bin/python
# sys-01.py

import sys
from sys import argv

print '''
Python version installed: {}

Python running on platforn: {}
'''.format(sys.version, sys.platform)

if len(argv) == 10:
	sys.exit('error: too many arguments')

print '''
argv = {}
len(argv) = {}
'''.format(argv, len(argv))

print 'Printing to stdout'
print >> sys.stderr, 'Printing to stderr'

print '''
total modules search path: {}
total modules loaded: {}
'''.format(len(sys.path), len(sys.modules))

# success
sys.exit(0)
```

>######
>```bash
>$ python sys-01.py

>Python version installed: 2.7.8 
[GCC 4.2.1 (Apple Inc. build 5664)]

>Python running on platforn: darwin

>argv = ['sys-01.py']
len(argv) = 1

>Printing to stdout.
Printing to stderr

>total modules search path: 23
total modules loaded: 42

> $ echo $?
0
```

#### [Learn more about sys module](https://docs.python.org/2.7/library/sys.html)

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

#### [Learn more about shutil module](https://docs.python.org/2.7/library/shutil.html)

--

### glob module — Unix style pathname pattern expansion

The `glob` module finds all the pathnames matching a specified pattern according to the rules used by the Unix shell.

- `glob.glob(pattern)` Return a list of path names that match the path pattern. Path can be absolute `/usr/local/bin/*.py` or relative `local/bin/*.py`.

>###### Example

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

#### [Learn more about glob module](https://docs.python.org/2.7/library/glob.html)

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

>###### Example

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
#### [Learn more about time module](https://docs.python.org/2.7/library/time.html)

--

## datetime module — Date and Time Value Manipulation

The `datetime` module includes functions and classes for doing date and time parsing, formatting, and arithmetic.


###### Commonly used functions:


- `datetime.date.today()` returns current date object without the time
- `datetime.datetime.today()` returns current date and time object
- `datetime.datetime.fromtimestamp(float)` convert unix timestamp to datetime object
- `datetime.timedelta` future and past dates can be calculated using basic arithmetic (+, -) on two datetime objects, or by combining a datetime with a timedelta object.

>###### Example

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
'Wed Apr 06 07:13:26 2016'

# convert formatted string to datetime object
>>> datetime.datetime.strptime('Wed Apr 06 07:13:26 2016', format)
datetime.datetime(2016, 4, 6, 7, 13, 26)
```

#### [Learn more about datetime module](https://docs.python.org/2.7/library/datetime.html)

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

Setting the shell argument to a true value causes subprocess to spawn a shell process (normally bash), which then runs the command. Using a shell means that variables, glob patterns, and other special shell features in the command string are processed before the command is run.

--

### Error Handling

The return value from `subprocess.call()` is the exit code of the program and is used to detect errors. The `subprocess.check_call()` function works like `call()`, except that the exit code is checked, and if it returns non-zero, then a `subprocess.CalledProcessError` exception is raised.

```python
#!/usr/bin/python
# check_call.py

import sys
import subprocess

try:
	cmd = 'false'
	print 'running command:',cmd
	subprocess.check_call(cmd, shell=True)
except subprocess.CalledProcessError as error:
	sys.exit('error: {}'.format(error))
```

>```bash
$ python check_call.py
running command: false
error: Command 'false' returned non-zero exit status 1
```

--

### Capturing Command Output

To run an external command and capture it's output, use `check_output(command, shell=True)` to capture the output for later processing. If command returns non-zero, then a `CalledProcessError` exception is raised similar to `check_call`.

>Execute `cat /etc/hosts` and write the output to a file `hosts.txt`

```python
#!/usr/bin/python
# capture_output.py

import subprocess
import sys

try:
	cmd = 'cat /etc/hosts'
	print 'running command:', cmd
	output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError as error:
	sys.exit('error: {}'.format(error))
else:
	print 'success!'
	with open('hosts.txt', 'w') as f:
		f.write(output)
```

By default, `check_output` captures outputs written to `stdout`. Setting the `stderr=subprocess.STDOUT` causes `stderr` outputs to redirected to `stdout`, so errors can be captured as well.

--
###  Working directory with Popen

The `call()`, `check_call()`, and `check_output()` are wrappers around the `Popen` class. Using `Popen` directly gives more control over how the command is run and how its input and output streams are processed.

#### One-Way Communication with a Process

To run a process and capture it's output, set the `stdout` and `stderr` arguments to `subprocess.PIPE` and call `communicate()`.

`communicate()` returns 2-tuple `(stderr_output, stderr_putput)`

```python
# one-way.py
import subprocess
import sys

script = sys.argv[0]

def main(argv):
	if not len(argv) == 1:
		sys.exit('usage: python {} command'.format(script))
	cmd = sys.argv[1]
	print 'running command:', cmd
	proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = proc.communicate()
	print '''
exit code: {}

stdout:
{}

stderr:
{}
'''.format(proc.poll(), stdout or None, stderr or None)

if __name__ == '__main__':
	main(sys.argv[1:])
```

>```bash
>$ python one-way.py 'grep 8080/tcp /etc/services'
>running command: grep 8080/tcp /etc/services

>exit code: 0

>stdout:
http-alt	8080/tcp     # HTTP Alternate (see port 80)

>stderr:
None
```

--

#### Bidirectional Communication with a Process

To set up the Popen instance for reading and writing at the same time, pass additional argument `stdin=subprocess.PIPE`.

```python
# bidirectional.py
import subprocess
from subprocess import PIPE
import sys

cmd = 'bc'
send = '1 + 1\n'

print 'running command:', cmd, 'and sending input:', send

proc = subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
stdout, stderr = proc.communicate(send)

print '''
exit code: {}

stdin:
{}

stdout:
{}

stderr:
{}
'''.format(proc.poll(), send, stdout or None, stderr or None)
```

>```bash
$ python bidirectional.py
running command: bc and sending input: 1 + 1

>exit code: 0

>stdin:
1 + 1

>stdout:
2

>stderr:
None
```

####[Learn more about subprocess module](https://docs.python.org/2.7/library/subprocess.html?highlight=subprocess#module-subprocess)

##Thank you! ;-)
