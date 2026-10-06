from __future__ import annotations

import argparse
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--port", type=int, default=24225)
    parser.add_argument("--context", default="vscode")
    parser.add_argument("--add-mode", default="query-projects")
    return parser.parse_args()


def port_is_open(port: int) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=0.25):
            return True
    except OSError:
        return False


def wait_for_port(port: int, timeout: float) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if port_is_open(port):
            return True
        time.sleep(0.5)
    return port_is_open(port)


def start_project_server(uv: str, port: int, timeout: float) -> None:
    log_path = Path(tempfile.gettempdir()) / "serena-project-server.log"
    process_options: dict[str, object] = {
        "stdin": subprocess.DEVNULL,
        "stdout": None,
        "stderr": subprocess.STDOUT,
    }
    if os.name == "nt":
        process_options["creationflags"] = (
            getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
            | getattr(subprocess, "CREATE_NO_WINDOW", 0)
        )
    else:
        process_options["start_new_session"] = True

    with log_path.open("ab") as log_file:
        process_options["stdout"] = log_file
        subprocess.Popen(
            [uv, "run", "--with", "serena-agent", "serena", "start-project-server"],
            **process_options,
        )

    if not wait_for_port(port, timeout):
        raise RuntimeError(
            f"Serena ProjectServer did not start on port {port}; see {log_path}"
        )


def main() -> int:
    args = parse_args()
    uv = shutil.which("uv")
    if uv is None:
        print("Serena launcher: uv was not found on PATH", file=sys.stderr)
        return 1

    project = args.project.expanduser()
    if not project.is_dir():
        print(f"Serena launcher: project directory does not exist: {project}", file=sys.stderr)
        return 1

    if not port_is_open(args.port):
        start_project_server(uv, args.port, timeout=15)

    return subprocess.call(
        [
            uv,
            "run",
            "--with",
            "serena-agent",
            "serena",
            "start-mcp-server",
            "--context",
            args.context,
            "--add-mode",
            args.add_mode,
            "--project",
            str(project),
        ]
    )
