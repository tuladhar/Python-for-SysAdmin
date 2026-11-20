# Building CLIs with `argparse`

`sys.argv` gets clumsy as soon as you need options. The built-in `argparse` module turns a few declarations into a real command-line tool with `--help`, type checking, defaults and helpful error messages.

Think about how `ls` works:

```bash
$ ls              # no arguments: list the current directory
$ ls -l /etc      # an optional flag and a positional argument
$ ls --help       # automatic help
```

`argparse` lets your scripts behave the same way.

## A first parser

```python
#!/usr/bin/env python3
# app.py
import argparse

parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument("integers", metavar="N", type=int, nargs="+",
                    help="an integer for the accumulator")
parser.add_argument("--sum", dest="accumulate", action="store_const",
                    const=sum, default=max,
                    help="sum the integers (default: find the max)")

args = parser.parse_args()
print(args.accumulate(args.integers))
```

```bash
$ python3 app.py -h
usage: app.py [-h] [--sum] N [N ...]

Process some integers.

positional arguments:
  N           an integer for the accumulator

options:
  -h, --help  show this help message and exit
  --sum       sum the integers (default: find the max)

$ python3 app.py 1 2 3 4
4
$ python3 app.py 1 2 3 4 --sum
10
$ python3 app.py one
usage: app.py [-h] [--sum] N [N ...]
app.py: error: argument N: invalid int value: 'one'
```

You wrote no help text formatting and no validation, and you still got both.

## The three steps

1. **Create a parser**: `parser = argparse.ArgumentParser(description="...")`
2. **Add arguments**: `parser.add_argument(...)` once per argument.
3. **Parse**: `args = parser.parse_args()` reads `sys.argv` and returns a namespace, so `args.port`, `args.verbose` and so on.

## The arguments you'll use most

```python
# positional (required)
parser.add_argument("host")

# option with a value and a default
parser.add_argument("-p", "--port", type=int, default=22)

# on/off flag
parser.add_argument("-v", "--verbose", action="store_true")

# restricted choices
parser.add_argument("--env", choices=["dev", "staging", "prod"], required=True)

# one or more values
parser.add_argument("files", nargs="+")
```

## Example: a TCP port checker

```python
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
```

```bash
$ python3 tcp_port_checker.py github.com -p 22 443 8080 -t 1
github.com:22    open
github.com:443   open
github.com:8080  CLOSED
```

## Subcommands

Tools like `git` and `kubectl` have subcommands (`git commit`, `git push`). Use `add_subparsers()`:

```python
parser = argparse.ArgumentParser(prog="svc")
sub = parser.add_subparsers(dest="command", required=True)

start = sub.add_parser("start", help="start a service")
start.add_argument("name")

status = sub.add_parser("status", help="show status")
status.add_argument("name", nargs="?", default="all")

args = parser.parse_args()
print(args.command, args.name)
```

## Useful `ArgumentParser` options

- `description` / `epilog`: text shown before / after the argument help.
- `prog`: the program name in usage messages (default: the script name).
- `formatter_class=argparse.ArgumentDefaultsHelpFormatter`: show default values in `--help` automatically.
- `parents=[...]`: reuse common arguments (like `--verbose`) across several parsers.

## Exercises

- Add a `--json` flag to `tcp_port_checker.py` that prints the results as JSON. You'll learn how in the [JSON chapter](11-json.md).
- Turn the `grep.py` exercise from [Command-line Arguments](04-command-line-arguments.md) into an `argparse` tool with `-i` (ignore case) and `-n` (line numbers).

[Learn more in the `argparse` documentation](https://docs.python.org/3/library/argparse.html)
