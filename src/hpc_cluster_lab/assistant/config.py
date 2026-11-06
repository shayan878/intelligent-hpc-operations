"""Environment-driven settings for the optional LLM cluster assistant."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from urllib.parse import urlparse

_NODE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")


@dataclass(frozen=True, slots=True)
class Settings:
    base_url: str
    model: str
    api_key: str | None = None
    timeout_seconds: float = 60.0
    allowed_nodes: tuple[str, ...] = ()
    max_tool_rounds: int = 6

    @classmethod
    def from_env(cls) -> "Settings":
        base_url = os.getenv("LLM_BASE_URL", "").strip().rstrip("/")
        model = os.getenv("LLM_MODEL", "").strip()
        if not base_url or not model:
            raise ValueError("LLM_BASE_URL and LLM_MODEL must be set in the environment")

        parsed = urlparse(base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("LLM_BASE_URL must be an absolute http(s) URL, including /v1")
        if parsed.scheme == "http" and parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
            raise ValueError("Use HTTPS for remote LLM endpoints; HTTP is allowed only on loopback")

        try:
            timeout_seconds = float(os.getenv("LLM_TIMEOUT_SECONDS", "60"))
        except ValueError as exc:
            raise ValueError("LLM_TIMEOUT_SECONDS must be a number") from exc
        if timeout_seconds <= 0:
            raise ValueError("LLM_TIMEOUT_SECONDS must be greater than zero")

        nodes = tuple(
            item.strip()
            for item in os.getenv("SLURM_ALLOWED_NODES", "").split(",")
            if item.strip()
        )
        invalid = [node for node in nodes if not _NODE_NAME.fullmatch(node)]
        if invalid:
            raise ValueError(f"Invalid node name(s) in SLURM_ALLOWED_NODES: {invalid}")
        if len(set(nodes)) != len(nodes):
            raise ValueError("SLURM_ALLOWED_NODES contains duplicate node names")

        return cls(
            base_url=base_url,
            model=model,
            api_key=os.getenv("LLM_API_KEY") or None,
            timeout_seconds=timeout_seconds,
            allowed_nodes=nodes,
        )
