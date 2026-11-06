"""Narrow subprocess adapter. Commands are fixed argv arrays; no shell is invoked."""

from __future__ import annotations

import re
import subprocess
from dataclasses import asdict, dataclass
from typing import Protocol

_JOB_ID = re.compile(r"^[0-9]+$")
_NODE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")


class CommandRunner(Protocol):
    def run(self, argv: list[str], timeout_seconds: float = 20.0) -> CommandResult: ...


@dataclass(frozen=True, slots=True)
class CommandResult:
    argv: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0

    def to_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["argv"] = list(self.argv)
        result["ok"] = self.ok
        return result


class SubprocessRunner:
    """Execute local Slurm client commands with a bounded timeout."""

    def run(self, argv: list[str], timeout_seconds: float = 20.0) -> CommandResult:
        try:
            completed = subprocess.run(
                argv,
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                shell=False,
            )
            return CommandResult(
                tuple(argv), completed.returncode, completed.stdout.strip(), completed.stderr.strip()
            )
        except FileNotFoundError as exc:
            return CommandResult(tuple(argv), 127, "", str(exc))
        except subprocess.TimeoutExpired as exc:
            return CommandResult(tuple(argv), 124, "", f"Command timed out: {exc}")


class SlurmController:
    """Allow-listed subset of Slurm controller operations."""

    def __init__(
        self,
        runner: CommandRunner | None = None,
        allowed_nodes: tuple[str, ...] = (),
    ) -> None:
        self._runner = runner or SubprocessRunner()
        self._allowed_nodes = frozenset(allowed_nodes)

    def _run(self, argv: list[str]) -> dict[str, object]:
        return self._runner.run(argv).to_dict()

    def get_cluster_status(self) -> dict[str, object]:
        return self._run(["sinfo", "-N", "-o", "%N|%T|%C|%m"])

    def get_active_jobs(self) -> dict[str, object]:
        return self._run(
            ["squeue", "-o", "%.18i %.12P %.20j %.10u %.2t %.10M %.6D %R"]
        )

    def get_job_details(self, job_id: str) -> dict[str, object]:
        if not _JOB_ID.fullmatch(job_id):
            raise ValueError("job_id must contain decimal digits only")
        return self._run(["scontrol", "show", "job", job_id])

    def validate_node(self, node_name: str) -> None:
        if not _NODE_NAME.fullmatch(node_name):
            raise ValueError("Invalid node name")
        if node_name not in self._allowed_nodes:
            raise PermissionError("Node is not present in SLURM_ALLOWED_NODES")

    def drain_node(self, node_name: str) -> dict[str, object]:
        self.validate_node(node_name)
        return self._run(
            [
                "scontrol", "update", f"NodeName={node_name}", "State=DRAIN",
                "Reason=OperatorApprovedMaintenance",
            ]
        )

    def resume_node(self, node_name: str) -> dict[str, object]:
        self.validate_node(node_name)
        return self._run(["scontrol", "update", f"NodeName={node_name}", "State=RESUME"])
