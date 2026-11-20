# The `sys` Module

The built-in `sys` module gives you access to the Python interpreter itself: its arguments, streams, version, platform and exit status.

```python
import sys
```

## Commonly used variables and functions

- `sys.argv` is the list of command-line arguments. *Covered in [Command-line Arguments](04-command-line-arguments.md).*
- `sys.exit(arg)` exits the program. `0` means success, any other number means failure, and a string is printed to `stderr` with exit code `1`.
- `sys.stdin`, `sys.stdout`, `sys.stderr` are the [standard streams](02-standard-io.md).
- `sys.version` / `sys.version_info` describe the running Python.
- `sys.platform` is the OS name, such as `linux` or `darwin` (macOS).
- `sys.executable` is the path to the Python binary that is running your script.
- `sys.path` is the list of directories Python searches when you `import`.
- `sys.modules` maps module names to modules that are already loaded.

## Example

```python
#!/usr/bin/env python3
# sys_01.py
import sys

print(f"Python version: {sys.version}")
print(f"Running on platform: {sys.platform}")
print(f"Interpreter: {sys.executable}")

if len(sys.argv) > 10:
    sys.exit("error: too many arguments")

print(f"argv = {sys.argv}")
print("Printing to stdout")
print("Printing to stderr", file=sys.stderr)

print(f"module search paths: {len(sys.path)}")
print(f"modules loaded: {len(sys.modules)}")

sys.exit(0)  # success
```

```bash
$ python3 sys_01.py
Python version: 3.13.0 (main, Oct  8 2026, 10:12:44) [GCC 14.2.1]
Running on platform: linux
Interpreter: /usr/bin/python3
argv = ['sys_01.py']
Printing to stdout
Printing to stderr
module search paths: 5
modules loaded: 37

$ echo $?
0
```

## Fail early on an old Python

If your script uses newer features, check the version at the top and exit with a clear message instead of a confusing `SyntaxError` later:

```python
import sys

if sys.version_info < (3, 10):
    sys.exit(f"this script needs Python 3.10+, you have {sys.version.split()[0]}")
```

## Exit codes matter

Cron, systemd, CI pipelines and shell scripts all look at your exit code to decide whether something failed. A script that prints "error" but exits with `0` is reported as a success.

```bash
$ python3 backup.py && echo "backup ok" || echo "backup FAILED"
```

## Exercises

- Write a script that exits with `0` if it runs on Linux and with `1` (and a message) everywhere else.
- Print every directory in `sys.path`, one per line, and mark the ones that don't exist.

[Learn more in the `sys` documentation](https://docs.python.org/3/library/sys.html)
