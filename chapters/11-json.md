# Working with JSON

JSON is how modern infrastructure talks: REST APIs, `kubectl get -o json`, `terraform show -json`, `docker inspect`, cloud CLIs. The built-in `json` module converts between JSON text and Python objects.

## JSON ↔ Python types

| JSON | Python |
| --- | --- |
| object `{}` | `dict` |
| array `[]` | `list` |
| string | `str` |
| number (int / real) | `int` / `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

## The four functions

- `json.loads(text)`: parse a JSON **string** into Python objects.
- `json.dumps(obj)`: turn Python objects into a JSON **string**.
- `json.load(file)`: parse JSON from an open **file**.
- `json.dump(obj, file)`: write JSON to an open **file**.

> The `s` stands for *string*. `load`/`dump` work with files.

```python
>>> import json
>>> data = json.loads('{"host": "web-01", "ports": [80, 443], "healthy": true}')
>>> data["ports"]
[80, 443]
>>> data["healthy"]
True
>>> json.dumps({"host": "web-01", "maintenance": None})
'{"host": "web-01", "maintenance": null}'
```

## Pretty printing

```python
>>> print(json.dumps(data, indent=2, sort_keys=True))
{
  "healthy": true,
  "host": "web-01",
  "ports": [
    80,
    443
  ]
}
```

From the shell, `python3 -m json.tool` validates and pretty-prints JSON, which is handy on a server without `jq`:

```bash
$ echo '{"a": 1, "b": [1, 2]}' | python3 -m json.tool
{
    "a": 1,
    "b": [
        1,
        2
    ]
}
$ python3 -m json.tool broken.json
Expecting ',' delimiter: line 3 column 5 (char 18)
```

## Reading and writing files

```python
import json

with open("inventory.json", encoding="utf-8") as f:
    inventory = json.load(f)

inventory["hosts"].append({"name": "db-02", "ip": "10.0.0.12"})

with open("inventory.json", "w", encoding="utf-8") as f:
    json.dump(inventory, f, indent=2)
```

## Handling bad JSON

`json.JSONDecodeError` tells you exactly where the problem is:

```python
try:
    config = json.loads('{"debug": true,}')
except json.JSONDecodeError as e:
    print(f"invalid JSON at line {e.lineno}, column {e.colno}: {e.msg}")
```

## Example: list containers that aren't running

`docker ps -a --format json` prints one JSON object per line. Combine `subprocess` and `json`:

```python
#!/usr/bin/env python3
# stopped_containers.py
import json
import subprocess

result = subprocess.run(
    ["docker", "ps", "-a", "--format", "json"],
    check=True, capture_output=True, text=True,
)

for line in result.stdout.splitlines():
    container = json.loads(line)
    if container["State"] != "running":
        print(f"{container['Names']:<30} {container['Status']}")
```

## Example: call a JSON API with only the standard library

```python
#!/usr/bin/env python3
# github_stars.py
import json
import os
import urllib.request

url = "https://api.github.com/repos/tuladhar/Python-for-SysAdmin"
request = urllib.request.Request(url)
token = os.environ.get("GITHUB_TOKEN")
if token:  # optional: raises the rate limit from 60 to 5,000 requests per hour
    request.add_header("Authorization", f"Bearer {token}")

with urllib.request.urlopen(request, timeout=10) as response:
    repo = json.load(response)

print(f"{repo['full_name']} has {repo['stargazers_count']} stars")
```

> Without a token, the GitHub API allows only 60 requests per hour per IP address. Shared networks (offices, CI runners) hit that limit quickly and get `HTTP Error 403: rate limit exceeded`. Reading secrets from environment variables, never from the script itself, keeps them out of Git.

## Exercises

- Run `kubectl get pods -A -o json` (or use a saved sample file) and print each pod's namespace, name and phase.
- Extend `tcp_port_checker.py` from the [argparse chapter](10-argparse.md) with a `--json` flag.

[Learn more in the `json` documentation](https://docs.python.org/3/library/json.html)
