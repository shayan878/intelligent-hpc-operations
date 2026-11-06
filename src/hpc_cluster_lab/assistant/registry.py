"""Validate and dispatch assistant tools, with an explicit approval boundary."""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from hpc_cluster_lab.assistant.schemas import tool_schemas
from hpc_cluster_lab.slurm.runner import SlurmController

ApprovalCallback = Callable[[str], bool]


class ToolRegistry:
    def __init__(
        self,
        controller: SlurmController,
        include_admin: bool = False,
        approval_callback: ApprovalCallback | None = None,
    ) -> None:
        self._controller = controller
        self._include_admin = include_admin
        self._approval_callback = approval_callback

    @property
    def schemas(self) -> list[dict[str, object]]:
        return tool_schemas(self._include_admin)

    @staticmethod
    def _parse_arguments(arguments: str | dict[str, Any]) -> dict[str, Any]:
        if isinstance(arguments, dict):
            parsed = arguments
        else:
            parsed = json.loads(arguments or "{}")
        if not isinstance(parsed, dict):
            raise ValueError("Tool arguments must be a JSON object")
        return parsed

    def execute(self, name: str, arguments: str | dict[str, Any]) -> dict[str, object]:
        try:
            args = self._parse_arguments(arguments)
            if name == "get_cluster_status":
                self._require_empty(args)
                return self._controller.get_cluster_status()
            if name == "get_active_jobs":
                self._require_empty(args)
                return self._controller.get_active_jobs()
            if name == "get_job_details":
                self._require_keys(args, {"job_id"})
                job_id = args.get("job_id")
                if not isinstance(job_id, str):
                    raise ValueError("job_id must be a string")
                return self._controller.get_job_details(job_id)
            if name in {"drain_node", "resume_node"}:
                return self._execute_admin(name, args)
            return {"ok": False, "error": f"Unknown tool: {name}"}
        except (ValueError, PermissionError, json.JSONDecodeError) as exc:
            return {"ok": False, "error": str(exc)}

    @staticmethod
    def _require_empty(args: dict[str, Any]) -> None:
        if args:
            raise ValueError("This tool does not accept arguments")

    @staticmethod
    def _require_keys(args: dict[str, Any], required: set[str]) -> None:
        if set(args) != required:
            raise ValueError(f"Expected exactly these argument keys: {sorted(required)}")

    def _execute_admin(self, name: str, args: dict[str, Any]) -> dict[str, object]:
        self._require_keys(args, {"node_name"})
        if not self._include_admin:
            return {"ok": False, "error": "Administrative tools are disabled for this session"}
        node_name = args.get("node_name")
        if not isinstance(node_name, str) or not node_name:
            raise ValueError("node_name must be a non-empty string")

        # Validate allow-list before prompting, so the model cannot solicit approval
        # for a node outside this operator's configured maintenance scope.
        self._controller.validate_node(node_name)
        if self._approval_callback is None:
            return {"ok": False, "error": "No interactive approval callback is configured"}

        verb = "drain" if name == "drain_node" else "resume"
        message = f"Approve {verb} operation for Slurm node '{node_name}'?"
        if not self._approval_callback(message):
            return {"ok": False, "denied": True, "error": "Operator declined the operation"}

        if name == "drain_node":
            return self._controller.drain_node(node_name)
        return self._controller.resume_node(node_name)
