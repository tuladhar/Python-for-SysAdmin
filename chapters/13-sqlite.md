# SQLite: a Database in a File

SQLite is a fast, reliable SQL database engine that stores everything in a single file and needs no server. It ships inside Python as the `sqlite3` module, so it's perfect for an inventory, a job history or a cache that your scripts can query with SQL.

```python
import sqlite3
```

## The basic workflow

1. `sqlite3.connect("file.db")` opens (or creates) a database file and returns a connection.
2. `connection.execute(sql, params)` runs a statement and returns a cursor.
3. `connection.commit()` saves your changes.
4. `cursor.fetchone()` / `cursor.fetchall()` read query results.
5. `connection.close()` closes the database.

```python
>>> import sqlite3
>>> con = sqlite3.connect("inventory.db")
>>> con.execute("""
...     CREATE TABLE IF NOT EXISTS hosts (
...         name TEXT PRIMARY KEY,
...         ip   TEXT NOT NULL,
...         role TEXT
...     )
... """)
>>> con.execute("INSERT INTO hosts VALUES (?, ?, ?)", ("web-01", "10.0.0.10", "web"))
>>> con.commit()
>>> con.execute("SELECT * FROM hosts").fetchall()
[('web-01', '10.0.0.10', 'web')]
```

Use `":memory:"` instead of a file name for a temporary in-memory database, which is handy for tests.

## Always use placeholders

Pass values with `?` placeholders, never with f-strings. The driver escapes them, which protects you from SQL injection and from names like `O'Brien`:

```python
role = "web"

# good
con.execute("SELECT * FROM hosts WHERE role = ?", (role,))

# bad: breaks on quotes and is an injection risk
con.execute(f"SELECT * FROM hosts WHERE role = '{role}'")
```

## Inserting many rows

```python
hosts = [
    ("web-02", "10.0.0.11", "web"),
    ("db-01", "10.0.0.20", "database"),
]
con.executemany("INSERT OR REPLACE INTO hosts VALUES (?, ?, ?)", hosts)
con.commit()
```

## Transactions with `with`

Using the connection as a context manager commits on success and rolls back if an exception is raised:

```python
with con:
    con.execute("UPDATE hosts SET role = ? WHERE name = ?", ("cache", "web-02"))
    con.execute("DELETE FROM hosts WHERE name = ?", ("old-01",))
```

> `with con:` handles the transaction, not the connection. Call `con.close()` when you're done.

## Rows by column name

Set `row_factory` to `sqlite3.Row` to access columns by name:

```python
con.row_factory = sqlite3.Row
for row in con.execute("SELECT name, ip FROM hosts ORDER BY name"):
    print(row["name"], row["ip"])
```

## Example: record every backup run

```python
#!/usr/bin/env python3
# backup_log.py
import sqlite3
import sys
from datetime import datetime, UTC

con = sqlite3.connect("backups.db")
con.execute("""
    CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY,
        started TEXT NOT NULL,
        target TEXT NOT NULL,
        ok INTEGER NOT NULL
    )
""")

if len(sys.argv) == 3:
    # record a run:  python3 backup_log.py /srv/data ok
    target, status = sys.argv[1], sys.argv[2]
    with con:
        con.execute(
            "INSERT INTO runs (started, target, ok) VALUES (?, ?, ?)",
            (datetime.now(UTC).isoformat(timespec="seconds"), target, status == "ok"),
        )

# report the last 5 runs
for started, target, ok in con.execute(
    "SELECT started, target, ok FROM runs ORDER BY id DESC LIMIT 5"
):
    print(f"{started}  {'OK  ' if ok else 'FAIL'}  {target}")

con.close()
```

You can also open the file with the `sqlite3` command-line tool and run any SQL you like:

```bash
$ sqlite3 backups.db "SELECT target, COUNT(*) FROM runs WHERE ok = 0 GROUP BY target"
```

## Exercises

- Load the `hosts.csv` file from the [CSV chapter](12-csv.md) into a `hosts` table.
- Add a `--failed` flag to `backup_log.py` that shows only failed runs.

[Learn more in the `sqlite3` documentation](https://docs.python.org/3/library/sqlite3.html)
