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
