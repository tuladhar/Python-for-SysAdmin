# Date and Time

Log timestamps, certificate expiry, backup retention, "how long did this job take?": you will deal with time constantly. Python gives you two modules for it.

## `time`: clocks and sleeping

- `time.time()` returns seconds since the Unix epoch as a float.
- `time.monotonic()` is a clock that never jumps backwards. Use it to **measure durations**.
- `time.sleep(seconds)` pauses the script.
- `time.ctime()` returns a human-readable local time string.
- `time.strftime(format)` formats the current local time.

```python
>>> import time
>>> time.time()
1795189224.396017
>>> time.ctime()
'Fri Nov 20 15:40:24 2026'
>>> time.strftime("%Y-%m-%d %H:%M:%S")
'2026-11-20 15:40:24'
```

### Measuring how long something takes

```python
import time

start = time.monotonic()
time.sleep(1.5)          # your slow task here
elapsed = time.monotonic() - start
print(f"took {elapsed:.2f}s")
```

> Don't use `time.time()` for durations. If NTP adjusts the system clock while your job runs, the result can be wrong or even negative.

## `datetime`: dates you can do math with

- `datetime.date.today()` returns today's date.
- `datetime.datetime.now(datetime.UTC)` returns the current date and time **in UTC**.
- `datetime.datetime.fromtimestamp(ts, datetime.UTC)` converts a Unix timestamp.
- `datetime.timedelta(days=7)` is a duration you can add to or subtract from a date.

```python
>>> from datetime import date, datetime, timedelta, UTC
>>> today = date.today()
>>> today - timedelta(days=10)     # past
datetime.date(2026, 11, 10)
>>> today + timedelta(days=10)     # future
datetime.date(2026, 11, 30)
>>> datetime.now(UTC).isoformat(timespec="seconds")
'2026-11-20T09:55:24+00:00'
```

> `datetime.UTC` was added in Python 3.11. On 3.10, use `datetime.timezone.utc`.

## Formatting and parsing

`strftime()` turns a datetime into text; `strptime()` parses text into a datetime.

```python
>>> fmt = "%a %b %d %H:%M:%S %Y"
>>> datetime.now().strftime(fmt)
'Fri Nov 20 15:40:24 2026'
>>> datetime.strptime("Mon Oct 14 17:56:24 2019", fmt)
datetime.datetime(2019, 10, 14, 17, 56, 24)
>>> datetime.fromisoformat("2026-11-20T09:55:24+00:00")
datetime.datetime(2026, 11, 20, 9, 55, 24, tzinfo=datetime.timezone.utc)
```

| Code | Meaning | Example |
| --- | --- | --- |
| `%Y-%m-%d` | date | `2026-11-20` |
| `%H:%M:%S` | time | `15:40:24` |
| `%a %b` | short day and month | `Fri Nov` |
| `%z` | UTC offset | `+0545` |

## Time zones

Store and compare times in **UTC**, and only convert to local time when you show them to a person. The `zoneinfo` module knows every time zone:

```python
>>> from zoneinfo import ZoneInfo
>>> now = datetime.now(UTC)
>>> now.astimezone(ZoneInfo("Asia/Kathmandu"))
datetime.datetime(2026, 11, 20, 15, 40, 24, tzinfo=zoneinfo.ZoneInfo(key='Asia/Kathmandu'))
```

## Example: delete backups older than 7 days

```python
#!/usr/bin/env python3
# prune_backups.py
import sys
from datetime import datetime, timedelta, UTC
from pathlib import Path

KEEP = timedelta(days=7)


def main(directory):
    cutoff = datetime.now(UTC) - KEEP
    for path in Path(directory).glob("*.tar.gz"):
        modified = datetime.fromtimestamp(path.stat().st_mtime, UTC)
        if modified < cutoff:
            print(f"deleting {path} (modified {modified:%Y-%m-%d})")
            path.unlink()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"usage: python3 {sys.argv[0]} BACKUP_DIR")
    main(sys.argv[1])
```

## Exercises

- Add a `--dry-run` mode to `prune_backups.py` that only prints what it would delete.
- Write a script that prints how many days are left until a date given as `YYYY-MM-DD`.

[Learn more in the `time`](https://docs.python.org/3/library/time.html) and [`datetime`](https://docs.python.org/3/library/datetime.html) documentation.
