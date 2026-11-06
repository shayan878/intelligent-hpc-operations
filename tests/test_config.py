import pytest

from hpc_cluster_lab.assistant.config import Settings


def test_settings_load_required_values_and_node_allowlist(monkeypatch):
    monkeypatch.setenv("LLM_BASE_URL", "http://localhost:8000/v1/")
    monkeypatch.setenv("LLM_MODEL", "lab-model")
    monkeypatch.setenv("LLM_API_KEY", "test-only-secret")
    monkeypatch.setenv("SLURM_ALLOWED_NODES", "worker1, worker2")
    settings = Settings.from_env()
    assert settings.base_url == "http://localhost:8000/v1"
    assert settings.model == "lab-model"
    assert settings.api_key == "test-only-secret"
    assert settings.allowed_nodes == ("worker1", "worker2")


def test_settings_reject_missing_endpoint(monkeypatch):
    monkeypatch.delenv("LLM_BASE_URL", raising=False)
    monkeypatch.delenv("LLM_MODEL", raising=False)
    with pytest.raises(ValueError):
        Settings.from_env()


def test_settings_reject_invalid_node_names(monkeypatch):
    monkeypatch.setenv("LLM_BASE_URL", "http://localhost:8000/v1")
    monkeypatch.setenv("LLM_MODEL", "lab-model")
    monkeypatch.setenv("SLURM_ALLOWED_NODES", "worker1; rm -rf /")
    with pytest.raises(ValueError):
        Settings.from_env()


def test_settings_reject_remote_http(monkeypatch):
    monkeypatch.setenv("LLM_BASE_URL", "http://llm.example.net/v1")
    monkeypatch.setenv("LLM_MODEL", "lab-model")
    with pytest.raises(ValueError, match="HTTPS"):
        Settings.from_env()


def test_settings_reject_non_positive_history_limit(monkeypatch):
    monkeypatch.setenv("LLM_BASE_URL", "http://localhost:8000/v1")
    monkeypatch.setenv("LLM_MODEL", "lab-model")
    monkeypatch.setenv("LLM_MAX_HISTORY_TURNS", "0")
    with pytest.raises(ValueError, match="at least 1"):
        Settings.from_env()


def test_settings_loads_history_limit(monkeypatch):
    monkeypatch.setenv("LLM_BASE_URL", "http://localhost:8000/v1")
    monkeypatch.setenv("LLM_MODEL", "lab-model")
    monkeypatch.setenv("LLM_MAX_HISTORY_TURNS", "5")
    assert Settings.from_env().max_history_turns == 5
