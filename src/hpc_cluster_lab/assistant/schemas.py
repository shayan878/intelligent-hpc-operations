"""JSON schemas for the narrow set of model-callable Slurm tools."""

from __future__ import annotations

READ_ONLY_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_cluster_status",
            "description": "Get a read-only summary of Slurm nodes and their states.",
            "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_active_jobs",
            "description": "List active and pending Slurm jobs using the current user's queue visibility.",
            "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_job_details",
            "description": "Inspect one numeric Slurm job ID. Do not guess job IDs.",
            "parameters": {
                "type": "object",
                "properties": {"job_id": {"type": "string", "pattern": "^[0-9]+$"}},
                "required": ["job_id"],
                "additionalProperties": False,
            },
        },
    },
]

ADMIN_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "drain_node",
            "description": "Request that an allow-listed Slurm worker stop accepting new jobs. Always explain why and wait for operator approval.",
            "parameters": {
                "type": "object",
                "properties": {"node_name": {"type": "string"}},
                "required": ["node_name"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "resume_node",
            "description": "Return an allow-listed worker to service after maintenance has been completed. Always explain why and wait for operator approval.",
            "parameters": {
                "type": "object",
                "properties": {"node_name": {"type": "string"}},
                "required": ["node_name"],
                "additionalProperties": False,
            },
        },
    },
]


def tool_schemas(include_admin: bool = False) -> list[dict[str, object]]:
    """Return only the tool schemas enabled for this assistant session."""
    return [*READ_ONLY_TOOLS, *(ADMIN_TOOLS if include_admin else [])]
