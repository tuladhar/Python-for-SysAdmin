"""Read-only networking exercises built on Python's standard library."""

from __future__ import annotations

import ipaddress
import socket
from dataclasses import dataclass


@dataclass(frozen=True)
class PortResult:
    host: str
    port: int
    open: bool
    error: str | None = None


def check_port(host: str, port: int, timeout: float = 1.0) -> PortResult:
    """Try one TCP connection without sending data or changing the host."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return PortResult(host, port, True)
    except (OSError, ValueError) as error:
        return PortResult(host, port, False, str(error))


def describe_subnet(cidr: str) -> dict[str, object]:
    """Explain a CIDR network using ipaddress (no packets are sent)."""
    network = ipaddress.ip_network(cidr, strict=False)
    hosts = list(network.hosts())
    return {
        "network": str(network.network_address),
        "broadcast": str(network.broadcast_address),
        "netmask": str(network.netmask),
        "prefix_length": network.prefixlen,
        "address_count": network.num_addresses,
        "usable_host_count": len(hosts),
        "first_host": str(hosts[0]) if hosts else None,
        "last_host": str(hosts[-1]) if hosts else None,
        "version": network.version,
    }
