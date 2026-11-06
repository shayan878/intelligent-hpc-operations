"""HTTP client for an OpenAI-compatible chat-completions endpoint."""

from __future__ import annotations

from typing import Any

import httpx

from hpc_cluster_lab.assistant.config import Settings


class OpenAICompatibleClient:
    def __init__(self, settings: Settings, transport: httpx.BaseTransport | None = None) -> None:
        self._settings = settings
        headers = {"Content-Type": "application/json"}
        if settings.api_key:
            headers["Authorization"] = f"Bearer {settings.api_key}"
        self._client = httpx.Client(
            timeout=httpx.Timeout(settings.timeout_seconds),
            headers=headers,
            transport=transport,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "OpenAICompatibleClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def complete(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self._settings.model,
            "messages": messages,
            "temperature": 0.1,
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        response = self._client.post(
            f"{self._settings.base_url}/chat/completions",
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
        choices = data.get("choices")
        if not isinstance(choices, list) or not choices:
            raise ValueError("LLM endpoint returned no chat-completion choices")
        message = choices[0].get("message")
        if not isinstance(message, dict):
            raise ValueError("LLM endpoint returned an invalid assistant message")
        return message
