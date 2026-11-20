# Standard Input, Output and Error

Every process on a Unix system starts with three open streams: standard input (`stdin`), standard output (`stdout`) and standard error (`stderr`). When you run a command in a terminal, all three are connected to that terminal.

- `print()` writes to `stdout`.
- Errors and tracebacks go to `stderr`.
- When your program reads input from the user or from a pipe, it reads `stdin`.

```bash
$ cat /etc/passwd | grep /bin/bash
#  \_ writes to stdout   \_ reads from stdin

$ ls no_such_file.txt
#  \_ writes to stderr
```

Keeping `stdout` for data and `stderr` for messages is what makes your scripts play nicely in pipelines: `script.py | sort` sorts the data, while errors still show up on screen.

## The `sys` streams

The built-in `sys` module exposes the three streams as file objects with `read()`, `readline()`, `readlines()` and `write()` methods.

```python
#!/usr/bin/env python3
# stdio.py
import sys

# write to stdout
print("Hello, world")
sys.stdout.write("Hello, world\n")

# write to stderr
print("Something went wrong", file=sys.stderr)
sys.stderr.write("Something went wrong\n")

# read a single line from stdin
username = input("Username: ")
print(f"Hi, {username}")

# read everything until EOF (press Ctrl-D in a terminal)
print("Enter a few lines and press Ctrl-D", file=sys.stderr)
lines = sys.stdin.readlines()
print("total lines read:", len(lines))
```

> `print(..., file=sys.stderr)` is the modern way to print errors. You'll still see `sys.stderr.write()` in older code; both work.

## Iterating over `stdin`

Most filters you write read `stdin` line by line. Iterating over `sys.stdin` does that without loading everything into memory, so it works on a 10 GB log file too:

```python
#!/usr/bin/env python3
# upper.py
import sys

for line in sys.stdin:
    sys.stdout.write(line.upper())
```

```bash
$ echo "hello sysadmin" | python3 upper.py
HELLO SYSADMIN
```

## Redirecting streams in the shell

Because your script uses the standard streams, the shell can redirect them:

```bash
$ python3 stdio.py > out.txt        # stdout to a file, stderr to screen
$ python3 stdio.py 2> errors.txt    # stderr to a file
$ python3 stdio.py > all.txt 2>&1   # both to the same file
```

## Exercises

- Write `count.py` that reads `stdin` and prints the number of lines, words and characters, like `wc`.
- Make it print a warning to `stderr` if the input is empty, and still print `0 0 0` to `stdout`.
