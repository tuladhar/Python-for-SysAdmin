#!/usr/bin/env python3
# tcp_port_checker.py
import argparse
import socket
import sys


def check(host, port, timeout):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def main():
    parser = argparse.ArgumentParser(description="Check if TCP ports are open.")
    parser.add_argument("host", help="hostname or IP address")
    parser.add_argument("-p", "--port", type=int, nargs="+", default=[22, 80, 443],
                        help="ports to check (default: 22 80 443)")
    parser.add_argument("-t", "--timeout", type=float, default=3.0,
                        help="seconds to wait per port (default: 3)")
    args = parser.parse_args()

    all_open = True
    for port in args.port:
        is_open = check(args.host, port, args.timeout)
        all_open = all_open and is_open
        print(f"{args.host}:{port:<5} {'open' if is_open else 'CLOSED'}")

    sys.exit(0 if all_open else 1)


if __name__ == "__main__":
    main()
