# Network Checks with `socket`

"Is the port open?" is one of the most common questions in operations. The built-in `socket` module answers it, and lets you resolve hostnames and talk to network services directly, without `telnet`, `nc` or `nslookup` installed.

```python
import socket
```

## Is a TCP port open?

`socket.create_connection()` resolves the host, connects, and raises `OSError` if it can't. Always pass a `timeout`, or a firewall that silently drops packets will make your script hang.

```python
#!/usr/bin/env python3
# port_check.py
import socket


def is_open(host, port, timeout=5):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


for host, port in [("google.com", 80), ("google.com", 81), ("localhost", 22)]:
    print(f"{host}:{port} is {'up' if is_open(host, port) else 'down'}")
```

```bash
$ python3 port_check.py
google.com:80 is up
google.com:81 is down
localhost:22 is up
```

> For a full CLI around this function, see the TCP port checker in the [argparse chapter](10-argparse.md).

## DNS lookups

```python
>>> import socket
>>> socket.gethostname()
'web-01'
>>> socket.gethostbyname("github.com")
'140.82.121.3'
>>> {info[4][0] for info in socket.getaddrinfo("google.com", 443)}   # IPv4 and IPv6
{'142.250.183.110', '2404:6800:4009:82a::200e'}
>>> socket.gethostbyaddr("1.1.1.1")[0]                               # reverse lookup
'one.one.one.one'
```

## Talking to a service

Once connected, you send and receive **bytes**. Here's a minimal HTTP request:

```python
import socket

with socket.create_connection(("example.com", 80), timeout=5) as s:
    s.sendall(b"HEAD / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n")
    response = s.recv(4096).decode()

print(response.splitlines()[0])   # HTTP/1.1 200 OK
```

## Checking many hosts in parallel

Checking 200 hosts one after another with a 5 second timeout can take minutes. `concurrent.futures` runs the checks in threads:

```python
#!/usr/bin/env python3
# sweep.py
from concurrent.futures import ThreadPoolExecutor
import socket


def is_open(target):
    host, port = target
    try:
        with socket.create_connection((host, port), timeout=2):
            return target, True
    except OSError:
        return target, False


targets = [(f"10.0.0.{i}", 22) for i in range(1, 255)]

with ThreadPoolExecutor(max_workers=50) as pool:
    for (host, port), up in pool.map(is_open, targets):
        if up:
            print(f"{host}:{port} open")
```

> Only scan networks you own or are allowed to test.

## Exercises

- Write `tls_expiry.py HOST` that prints how many days are left on a server's TLS certificate. Hint: `ssl.create_default_context().wrap_socket(...)` and `getpeercert()["notAfter"]`.
- Read hosts and ports from a CSV file and write a CSV report of which are reachable.

[Learn more in the `socket` documentation](https://docs.python.org/3/library/socket.html)
