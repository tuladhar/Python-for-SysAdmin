# Running Commands with `subprocess`

Sooner or later your script needs to run `systemctl`, `git`, `kubectl` or `df`. The `subprocess` module starts other programs, passes them input, captures their output and gives you their exit code.

## `subprocess.run()`: the one function you need

Since Python 3.5, `subprocess.run()` is the recommended way to run a command. It waits for the command to finish and returns a `CompletedProcess` object.

```python
>>> import subprocess
>>> result = subprocess.run(["ls", "-l", "/etc/hosts"])
-rw-r--r-- 1 root root 475 Nov 20 09:12 /etc/hosts
>>> result.returncode
0
```

Pass the command as a **list** of arguments. Python runs the program directly, without a shell, so a filename like `my file; rm -rf ~` is just a strange filename, not a second command.

## Capturing output

Add `capture_output=True` to collect `stdout` and `stderr`, and `text=True` to get strings instead of bytes:

```python
>>> result = subprocess.run(["uname", "-r"], capture_output=True, text=True)
>>> result.stdout.strip()
'6.12.8-200.fc41.x86_64'
>>> result.stderr
''
```

## Failing on errors

By default, `run()` doesn't care if the command fails; you have to check `returncode`. Add `check=True` to raise `CalledProcessError` on any non-zero exit code:

```python
#!/usr/bin/env python3
# check_call.py
import subprocess
import sys

cmd = ["ls", "/no/such/dir"]
print("running command:", " ".join(cmd))

try:
    subprocess.run(cmd, check=True, capture_output=True, text=True)
except subprocess.CalledProcessError as e:
    sys.exit(f"error: exit code {e.returncode}: {e.stderr.strip()}")
```

```bash
$ python3 check_call.py
running command: ls /no/such/dir
error: exit code 2: ls: cannot access '/no/such/dir': No such file or directory
```

Two more errors are worth catching in real scripts:

- `FileNotFoundError` if the program isn't installed.
- `subprocess.TimeoutExpired` if you pass `timeout=` and the command hangs.

```python
import subprocess
import sys

try:
    subprocess.run(["ping", "-c", "1", "10.0.0.1"], check=True, timeout=5)
except FileNotFoundError:
    sys.exit("ping is not installed")
except subprocess.TimeoutExpired:
    sys.exit("host did not answer within 5 seconds")
except subprocess.CalledProcessError:
    sys.exit("host is unreachable")
```

## Sending input

Use `input=` to write to the command's `stdin`:

```python
>>> result = subprocess.run(["sort"], input="web-02\nweb-01\n", capture_output=True, text=True)
>>> result.stdout
'web-01\nweb-02\n'
```

## When you need a shell

Pipes (`|`), globs (`*.log`), `&&` and environment variable expansion are **shell features**. They only work with `shell=True` and a string command:

```python
subprocess.run("grep -c bash /etc/passwd | tee count.txt", shell=True, check=True)
```

> Never build a `shell=True` command from user input or file content. A value like `x; rm -rf /` would run as a second command. If you must, quote each value with `shlex.quote()`. Usually you can avoid the shell completely: use `glob` for wildcards and Python for the filtering.

## Example: capture output and save it to a file

```python
#!/usr/bin/env python3
# capture_output.py
import subprocess
import sys
from pathlib import Path

cmd = ["cat", "/etc/hosts"]
print("running command:", " ".join(cmd))

try:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
except subprocess.CalledProcessError as e:
    sys.exit(f"error: {e.stderr}")

Path("hosts.txt").write_text(result.stdout, encoding="utf-8")
print("success! wrote", len(result.stdout), "characters to hosts.txt")
```

## Streaming output with `Popen`

`run()` waits until the command finishes. For long-running commands, such as following a log or a deployment, use `Popen` to read output **while** the command runs:

```python
#!/usr/bin/env python3
# follow.py
import subprocess

with subprocess.Popen(
    ["ping", "-c", "5", "1.1.1.1"],
    stdout=subprocess.PIPE,
    text=True,
) as proc:
    for line in proc.stdout:
        print("ping says:", line.rstrip())

print("exit code:", proc.returncode)
```

## Old API cheat sheet

You will find these in older scripts and Stack Overflow answers. They still work, but `run()` covers all of them:

| Old | Modern equivalent |
| --- | --- |
| `subprocess.call(cmd)` | `subprocess.run(cmd).returncode` |
| `subprocess.check_call(cmd)` | `subprocess.run(cmd, check=True)` |
| `subprocess.check_output(cmd)` | `subprocess.run(cmd, check=True, capture_output=True).stdout` |
| `os.system("cmd")` | `subprocess.run(["cmd"])` |

## Exercises

- Write `svc_status.py SERVICE...` that runs `systemctl is-active` for each service and prints a table of `active` / `inactive`.
- Run `df -P` and parse its output into a list of dictionaries. Then compare the result with `shutil.disk_usage()` from the [shutil chapter](07-shutil-and-glob.md).

[Learn more in the `subprocess` documentation](https://docs.python.org/3/library/subprocess.html)
