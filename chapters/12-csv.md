# Working with CSV

CSV (comma-separated values, [RFC 4180](https://www.rfc-editor.org/rfc/rfc4180)) is still everywhere: asset inventories, billing exports, user lists from HR, reports your manager wants in a spreadsheet. The built-in `csv` module reads and writes it correctly, including quoted fields with commas inside.

```csv
hostname,ip,role
web-01,10.0.0.10,web
web-02,10.0.0.11,web
db-01,10.0.0.20,"database, primary"
```

> Don't parse CSV with `line.split(",")`. It breaks as soon as a field contains a comma, like `"database, primary"` above.

## Reading rows as lists

```python
import csv

with open("hosts.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)          # skip the header row
    for row in reader:
        print(row[0], row[1])
```

Always open CSV files with `newline=""`. The `csv` module handles line endings itself.

## Reading rows as dictionaries

`csv.DictReader` uses the header row as keys, so you can refer to columns by name. It reads the header automatically.

```python
import csv

with open("hosts.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(f"{row['hostname']:<10} {row['ip']:<12} {row['role']}")
```

```text
web-01     10.0.0.10    web
web-02     10.0.0.11    web
db-01      10.0.0.20    database, primary
```

## Writing CSV

```python
import csv

rows = [
    {"hostname": "web-01", "ip": "10.0.0.10", "role": "web"},
    {"hostname": "db-01", "ip": "10.0.0.20", "role": "database, primary"},
]

with open("hosts.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["hostname", "ip", "role"])
    writer.writeheader()
    writer.writerows(rows)
```

Use `csv.writer` and `writer.writerow([...])` if you're working with lists instead of dictionaries.

## Other delimiters

Many "CSV" files are really tab- or semicolon-separated. Pass `delimiter`, e.g. `delimiter="\t"` or `delimiter=";"`:

```python
import csv
import io

tsv = io.StringIO("web-01\t10.0.0.10\nweb-02\t10.0.0.11\n")  # stands in for an open file
for row in csv.reader(tsv, delimiter="\t"):
    print(row)
```

## Example: export local users to CSV

`/etc/passwd` is a colon-separated file, so `csv` can read it too:

```python
#!/usr/bin/env python3
# users_to_csv.py
import csv
import sys

fields = ["user", "password", "uid", "gid", "comment", "home", "shell"]

with open("/etc/passwd", newline="", encoding="utf-8") as f:
    users = [dict(zip(fields, row)) for row in csv.reader(f, delimiter=":", quoting=csv.QUOTE_NONE)]

writer = csv.DictWriter(sys.stdout, fieldnames=["user", "uid", "home", "shell"],
                        extrasaction="ignore")
writer.writeheader()
writer.writerows(u for u in users if int(u["uid"]) >= 1000)
```

```bash
$ python3 users_to_csv.py > users.csv
```

## Exercises

- Read `hosts.csv` and check that every `ip` column is a valid address. Hint: `ipaddress.ip_address()`.
- Combine this chapter with the [argparse chapter](10-argparse.md): run the TCP port checker for every host in a CSV file and write the results to a new CSV.

[Learn more in the `csv` documentation](https://docs.python.org/3/library/csv.html)
