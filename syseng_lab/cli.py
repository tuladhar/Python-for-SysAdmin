"""Command-line interface for the systems engineering learning lab."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence

from . import __version__
from .network import check_port, describe_subnet
from .system import collect_system_info, disk_usage


LESSONS = {
    "system-info": "Inspect a machine with platform, socket, and os modules.",
    "disk-usage": "Measure storage and practice thresholds and structured output.",
    "check-ports": "Check TCP reachability with timeouts and error handling.",
    "subnet": "Understand CIDR, network addresses, and usable hosts.",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m syseng_lab",
        description="Beginner-friendly systems and network engineering exercises.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("lessons", help="Show the recommended learning path.")
    subparsers.add_parser("system-info", help="Show read-only local system information.")

    disk_parser = subparsers.add_parser("disk-usage", help="Show disk usage for a path.")
    disk_parser.add_argument("path", nargs="?", default=".")
    disk_parser.add_argument(
        "--warning",
        type=float,
        default=80.0,
        help="Exit with status 1 when usage reaches this percentage (default: 80).",
    )

    ports_parser = subparsers.add_parser("check-ports", help="Check TCP ports on a host.")
    ports_parser.add_argument("host")
    ports_parser.add_argument("ports", nargs="+", type=int)
    ports_parser.add_argument("--timeout", type=float, default=1.0)

    subnet_parser = subparsers.add_parser("subnet", help="Describe an IPv4 or IPv6 CIDR.")
    subnet_parser.add_argument("cidr")
    return parser


def print_json(value: object) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def run(args: argparse.Namespace) -> int:
    if args.command == "lessons":
        for number, (name, description) in enumerate(LESSONS.items(), 1):
            print(f"{number}. {name}: {description}")
        return 0

    if args.command == "system-info":
        print_json(collect_system_info().as_dict())
        return 0

    if args.command == "disk-usage":
        if not 0 <= args.warning <= 100:
            print("--warning must be between 0 and 100.", file=sys.stderr)
            return 2
        try:
            result = disk_usage(args.path)
        except OSError as error:
            print(f"Could not inspect {args.path!r}: {error}", file=sys.stderr)
            return 2
        print_json(result)
        return int(result["used_percent"] >= args.warning)

    if args.command == "check-ports":
        if not 0 < args.timeout:
            print("--timeout must be greater than zero.", file=sys.stderr)
            return 2
        results = [check_port(args.host, port, args.timeout) for port in args.ports]
        print_json([result.__dict__ for result in results])
        return int(any(not result.open for result in results))

    if args.command == "subnet":
        try:
            print_json(describe_subnet(args.cidr))
        except ValueError as error:
            print(f"Invalid CIDR {args.cidr!r}: {error}", file=sys.stderr)
            return 2
        return 0

    return 2


def main(argv: Sequence[str] | None = None) -> None:
    raise SystemExit(run(build_parser().parse_args(argv)))
