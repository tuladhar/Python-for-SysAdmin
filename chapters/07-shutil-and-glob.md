# Shell Utilities: `shutil` and `glob`

Two modules replace most of the file-shuffling you do with `cp`, `mv`, `rm -r`, `df` and shell wildcards.

## `shutil`: high-level file operations

### Copy

- `shutil.copy(src, dst)` copies a file's content and permission bits. `dst` can be a directory.
- `shutil.copy2(src, dst)` also copies timestamps, like `cp -p`.
- `shutil.copytree(src, dst)` copies a whole directory tree, like `cp -r`.

### Move and delete

- `shutil.move(src, dst)` moves a file or directory, like `mv`.
- `shutil.rmtree(path)` deletes a directory tree, like `rm -rf`. **There is no undo.**

### Disk, commands and archives

- `shutil.disk_usage(path)` returns `(total, used, free)` in bytes, like `df`.
- `shutil.which("cmd")` returns the full path of a command, or `None`, like `which`.
- `shutil.make_archive(base, "gztar", root_dir)` creates a `.tar.gz` (or `zip`) archive.
- `shutil.chown(path, user, group)` changes ownership, like `chown`.

```python
>>> import shutil
>>> shutil.copy2("/etc/hosts", "/tmp/hosts.bak")
'/tmp/hosts.bak'
>>> shutil.which("docker")
'/usr/bin/docker'
>>> total, used, free = shutil.disk_usage("/")
>>> f"{used / total:.0%} used"
'63% used'
>>> shutil.make_archive("/tmp/home-backup", "gztar", ".")   # archive the current directory
'/tmp/home-backup.tar.gz'
```

> Copying or archiving system directories like `/etc/ssh` raises `PermissionError` as a normal user, because some files (such as SSH host keys) are readable only by root. Run the script with `sudo`, or catch the error and skip those files.

## Example: alert when the disk is almost full

```python
#!/usr/bin/env python3
# disk_alert.py
import shutil
import sys

THRESHOLD = 80  # percent


def main(path="/"):
    total, used, free = shutil.disk_usage(path)
    percent = used / total * 100
    print(f"{path}: {percent:.1f}% used, {free / 2**30:.1f} GiB free")
    if percent > THRESHOLD:
        # a non-zero exit code lets cron, systemd or your monitoring react
        sys.exit(f"WARNING: {path} is above {THRESHOLD}%")


if __name__ == "__main__":
    main(*sys.argv[1:])
```

> The original version of this example also sends an email with `smtplib`. See [`examples/Monitoring Disk Space and Sending Alerts.py`](https://github.com/tuladhar/Python-for-SysAdmin/blob/main/examples/Monitoring%20Disk%20Space%20and%20Sending%20Alerts.py).

## `glob`: Unix-style wildcards

`glob.glob(pattern)` returns the paths that match a shell-style pattern. Use `**` with `recursive=True` to search subdirectories.

```python
>>> import glob
>>> glob.glob("/etc/*.conf")
['/etc/resolv.conf', '/etc/sudo.conf', '/etc/host.conf', '/etc/logrotate.conf']
>>> glob.glob("/var/log/**/*.log", recursive=True)
['/var/log/dnf.log', '/var/log/nginx/access.log', '/var/log/nginx/error.log']
```

`pathlib` has the same feature built in: `Path("/var/log").rglob("*.log")`.

## Exercises

- Write `rotate.py` that gzips every `*.log` file older than 7 days in a directory. Hint: `os.stat(path).st_mtime`, `time.time()` and `shutil.copyfileobj` with `gzip.open`.
- Make `disk_alert.py` check every path given on the command line and exit non-zero if any of them is over the threshold.

[Learn more in the `shutil`](https://docs.python.org/3/library/shutil.html) and [`glob`](https://docs.python.org/3/library/glob.html) documentation.
