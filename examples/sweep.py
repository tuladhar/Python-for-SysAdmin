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
