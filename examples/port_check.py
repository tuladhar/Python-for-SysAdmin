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
