# Working with Files

Config files, logs, inventories, CSV exports: most sysadmin scripts start by reading a file. Python's built-in `open()` is the standard interface for that.

```python
open(file, mode="r", encoding=None)
```

- **file**: an absolute or relative path, such as `/etc/passwd` or `./ip-list.txt`.
- **mode**: how to open the file. The default is `r` (read, text mode).
- **encoding**: always pass `encoding="utf-8"` for text files, so your script behaves the same on every machine.

| Mode | Meaning |
| --- | --- |
| `r` | read (default) |
| `w` | write, **truncating** the file if it exists |
| `x` | create a new file, fail if it already exists |
| `a` | append to the end of the file |
| `+` | read and write, e.g. `r+` |
| `b` | binary mode, returns `bytes` instead of `str` |

## Always use `with`

The `with` statement closes the file for you, even when an exception is raised. There is almost never a reason to call `.close()` by hand.

```python
# reading a file line by line
with open("/etc/passwd", encoding="utf-8") as f:
    for line in f:
        print(len(line), line.rstrip())

# writing a file
with open("hosts.txt", "w", encoding="utf-8") as f:
    f.write("127.0.0.1\n")
    f.writelines(["1.1.1.1\n", "8.8.8.8\n"])
```

Useful file object methods:

- `.read()` reads the whole file as one string.
- `.readline()` reads a single line.
- `.readlines()` returns all lines as a list.
- `.write(text)` writes a string and returns the number of characters written.
- `.writelines(lines)` writes every string in a list.

## Handling errors

Missing files, wrong permissions and directories all raise subclasses of `OSError`. Catch the specific one when you can:

```python
try:
    with open("/etc/shadow", encoding="utf-8") as f:
        print(f.read())
except FileNotFoundError:
    print("no such file")
except PermissionError:
    print("permission denied, try with sudo")
except OSError as e:
    print(f"could not read file: {e}")
```

## Example: find users with a bash shell

Read `/etc/passwd` and print every line (with its line number) whose shell is `/bin/bash`:

```python
#!/usr/bin/env python3
# working_with_files_01.py
import sys


def main():
    try:
        with open("/etc/passwd", encoding="utf-8") as f:
            for no, line in enumerate(f, start=1):
                if line.rstrip().endswith("/bin/bash"):
                    print(f"{no} {line.rstrip()}")
    except OSError as e:
        sys.exit(f"error: {e}")


if __name__ == "__main__":
    main()
```

## The modern way: `pathlib`

`pathlib.Path` wraps a path in an object with handy methods. For quick reads and writes it is shorter than `open()`:

```python
from pathlib import Path

hosts = Path("/etc/hosts")
print(hosts.exists(), hosts.stat().st_size)

text = hosts.read_text(encoding="utf-8")
Path("hosts.bak").write_text(text, encoding="utf-8")

# all .conf files in /etc
for conf in Path("/etc").glob("*.conf"):
    print(conf.name)
```

## Reading many files with `fileinput`

The `fileinput` module loops over the lines of every file given on the command line, or over `stdin` if no files are given. That's exactly how tools like `cat` and `grep` behave.

```python
#!/usr/bin/env python3
# line_count.py
import fileinput

lines = 0
for line in fileinput.input(encoding="utf-8"):
    lines += 1

print("total lines:", lines)
```

```bash
$ cat /etc/passwd | python3 line_count.py
total lines: 41
$ python3 line_count.py /etc/services /etc/passwd /etc/hosts
total lines: 11520
```

## Exercises

- Write `tail.py FILE N` that prints the last `N` lines of a file. Hint: `collections.deque(f, maxlen=n)`.
- Write a script that backs up `/etc/hosts` to `hosts.YYYY-MM-DD.bak` before you edit it.
