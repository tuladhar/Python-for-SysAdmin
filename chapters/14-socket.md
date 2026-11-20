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


def is_open(host, port, timeout=3):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


for host, port in [("github.com", 443), ("github.com", 8080), ("localhost", 22)]:
    print(f"{host}:{port} is {'up' if is_open(host, port) else 'down'}", flush=True)
```

```bash
$ python3 port_check.py
github.com:443 is up
github.com:8080 is down
localhost:22 is up
```

> The timeout applies to **each address** the name resolves to. `google.com` has a dozen IPv4 and IPv6 addresses, so a closed port there can take `12 × timeout` to report as down. Keep timeouts short, or check a specific IP.

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
import ipaddress
import socket
import sys
from concurrent.futures import ThreadPoolExecutor


def is_open(target):
    host, port = target
    try:
        with socket.create_connection((host, port), timeout=1):
            return target, True
    except OSError:
        return target, False


def main(argv):
    if len(argv) != 2:
        sys.exit(f"usage: python3 {sys.argv[0]} NETWORK PORT   e.g. 172.16.0.0/24 22")
    network, port = ipaddress.ip_network(argv[0], strict=False), int(argv[1])
    targets = [(str(ip), port) for ip in network.hosts()]

    with ThreadPoolExecutor(max_workers=50) as pool:
        for (host, port), up in pool.map(is_open, targets):
            if up:
                print(f"{host}:{port} open")


if __name__ == "__main__":
    main(sys.argv[1:])
```

Find your own network with `ip -4 addr`. In the iximiuz Labs playground it is `172.16.0.0/24`:

```bash
$ ip -4 -o addr show eth0
2: eth0    inet 172.16.0.2/24 ...
$ python3 sweep.py 172.16.0.0/24 22
172.16.0.2:22 open
```

> Only scan networks you own or are allowed to test.

## Exercises

- Write `tls_expiry.py HOST` that prints how many days are left on a server's TLS certificate. Hint: `ssl.create_default_context().wrap_socket(...)` and `getpeercert()["notAfter"]`.
- Read hosts and ports from a CSV file and write a CSV report of which are reachable.

[Learn more in the `socket` documentation](https://docs.python.org/3/library/socket.html)
