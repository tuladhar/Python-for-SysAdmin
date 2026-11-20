# The `os` Module

The built-in `os` module exposes operating system functionality (environment variables, files, directories, processes) in a portable way, so the same script runs on Linux, macOS and Windows.

```python
import os
```

## Environment variables

- `os.environ` is a dictionary-like mapping of the environment, e.g. `os.environ["HOME"]`.
- `os.environ.get("KEY", "default")` (or `os.getenv`) returns a default instead of raising `KeyError`.
- Assign to `os.environ["KEY"]` to change a variable for the current process and any child processes it starts.

```python
>>> import os
>>> os.environ.get("SHELL")
'/bin/bash'
>>> os.getenv("NO_SUCH_VAR", "fallback")
'fallback'
>>> os.environ["APP_ENV"] = "staging"   # visible to subprocesses you start
```

> Reading configuration from environment variables (like `DATABASE_URL`) is the standard way to configure scripts in containers and CI pipelines.

## Files and directories

- `os.getcwd()` returns the current working directory, like `pwd`.
- `os.chdir(path)` changes it, like `cd`.
- `os.listdir(path)` lists entries in a directory.
- `os.makedirs(path, exist_ok=True)` creates a directory tree, like `mkdir -p`.
- `os.remove(path)` / `os.rmdir(path)` delete a file / empty directory.
- `os.stat(path)` returns size, permissions, owner and timestamps, like `stat`.
- `os.walk(path)` walks a directory tree recursively, like `find`. It yields `(dirpath, dirnames, filenames)` tuples.

```python
>>> import os, tempfile, datetime
>>> fd, temp = tempfile.mkstemp()      # safely create a temporary file
>>> with os.fdopen(fd, "w") as f:
...     f.write("test\n")
>>> st = os.stat(temp)
>>> st.st_size, oct(st.st_mode)
(5, '0o100600')
>>> datetime.datetime.fromtimestamp(st.st_mtime)
datetime.datetime(2026, 11, 20, 15, 42, 7, 120394)
```

> Use the `tempfile` module (`mkstemp()`, `TemporaryDirectory()`) for temporary files. Old functions like `os.tmpnam` and `tempfile.mktemp` are insecure and have been removed or deprecated.

## Path names with `os.path`

- `os.path.join(a, b)` joins path parts with the right separator.
- `os.path.abspath(path)` returns the absolute path.
- `os.path.basename(path)` / `os.path.dirname(path)` return the file / directory part.
- `os.path.exists(path)`, `os.path.isfile(path)`, `os.path.isdir(path)` test a path.
- `os.path.getsize(path)` returns the size in bytes.

```python
>>> os.path.isdir("/etc")
True
>>> os.path.basename("/etc/passwd"), os.path.dirname("/etc/passwd")
('passwd', '/etc')
>>> os.path.getsize("/etc/hosts")
475
```

`pathlib` does the same with objects instead of strings, and is the recommended style for new code:

```python
>>> from pathlib import Path
>>> p = Path("/etc/passwd")
>>> p.name, p.parent, p.suffix
('passwd', PosixPath('/etc'), '')
>>> p.is_file(), p.stat().st_size
(True, 2861)
>>> Path.home() / ".ssh" / "config"
PosixPath('/home/puru/.ssh/config')
```

## Processes and system information

- `os.getpid()` / `os.getppid()` return the current and parent process ID.
- `os.uname()` returns system name, hostname, kernel release, version and machine, like `uname -a`.
- `os.getloadavg()` returns the 1, 5 and 15 minute load average.
- `os.cpu_count()` returns the number of CPUs.

```python
>>> os.uname().nodename
'web-01'
>>> os.getloadavg()
(0.42, 0.37, 0.31)
>>> os.cpu_count()
4
```

> To run other commands, don't use `os.system()`. Use the [`subprocess`](09-subprocess.md) module, which gives you the exit code and output safely.

## Example: print the size of every file in a directory

```python
#!/usr/bin/env python3
# filesizes.py
import os
import sys


def filesizes(path):
    """Print the size in bytes of each file under path."""
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                size = os.path.getsize(filepath)
            except OSError:
                continue  # broken symlink or file removed meanwhile
            print(f"{size:>10} {filepath}")


def main(argv):
    if len(argv) != 1:
        sys.exit(f"usage: python3 {sys.argv[0]} DIR")
    filesizes(argv[0])


if __name__ == "__main__":
    main(sys.argv[1:])
```

```bash
$ python3 filesizes.py /etc/ssh
       573 /etc/ssh/ssh_config
      3289 /etc/ssh/sshd_config
       ...
```

## Exercises

- Change `filesizes.py` to print only the 10 largest files. Hint: collect `(size, path)` tuples and use `sorted(..., reverse=True)[:10]`.
- Print the sizes in human-readable units (`K`, `M`, `G`), like `du -h`.
- Rewrite it with `Path(path).rglob("*")` instead of `os.walk`.

[Learn more in the `os` documentation](https://docs.python.org/3/library/os.html)
