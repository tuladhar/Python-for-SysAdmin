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
