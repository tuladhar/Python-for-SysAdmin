"""Small, cross-platform system inspection helpers."""

from __future__ import annotations

import getpass
import os
import platform
import shutil
import socket
import sys
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class SystemInfo:
    hostname: str
    user: str
    operating_system: str
    release: str
    python_version: str
    cpu_count: int | None

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def collect_system_info() -> SystemInfo:
    """Collect safe, read-only facts about the current machine."""
    return SystemInfo(
        hostname=socket.gethostname(),
        user=getpass.getuser(),
        operating_system=platform.system() or "Unknown",
        release=platform.release() or "Unknown",
        python_version=platform.python_version(),
        cpu_count=os.cpu_count(),
    )


def disk_usage(path: str) -> dict[str, object]:
    """Return disk usage for *path*, with values suitable for JSON output."""
    usage = shutil.disk_usage(path)
    percent = (usage.used / usage.total * 100) if usage.total else 0.0
    return {
        "path": path,
        "total_bytes": usage.total,
        "used_bytes": usage.used,
        "free_bytes": usage.free,
        "used_percent": round(percent, 2),
    }
