import json

from hpc_cluster_lab.assistant.registry import ToolRegistry
from hpc_cluster_lab.slurm.runner import CommandResult


class FakeRunner:
    def __init__(self):
        self.calls = []

    def run(self, argv, timeout_seconds=20.0):
        self.calls.append(argv)
        return CommandResult(tuple(argv), 0, "done", "")


def test_admin_tools_hidden_by_default():
    runner = FakeRunner()
    from hpc_cluster_lab.slurm.runner import SlurmController

    registry = ToolRegistry(SlurmController(runner, ("worker1",)))
    assert "drain_node" not in [x["function"]["name"] for x in registry.schemas]
    result = registry.execute("drain_node", {"node_name": "worker1"})
    assert result["ok"] is False
    assert runner.calls == []


def test_admin_tool_requires_explicit_approval():
    runner = FakeRunner()
    from hpc_cluster_lab.slurm.runner import SlurmController

    prompts = []
    registry = ToolRegistry(
        SlurmController(runner, ("worker1",)),
        include_admin=True,
        approval_callback=lambda prompt: prompts.append(prompt) or False,
    )
    result = registry.execute("drain_node", json.dumps({"node_name": "worker1"}))
    assert result["denied"] is True
    assert "worker1" in prompts[0]
    assert runner.calls == []


def test_approved_admin_tool_runs_fixed_command():
    runner = FakeRunner()
    from hpc_cluster_lab.slurm.runner import SlurmController

    registry = ToolRegistry(
        SlurmController(runner, ("worker1",)),
        include_admin=True,
        approval_callback=lambda _: True,
    )
    result = registry.execute("resume_node", {"node_name": "worker1"})
    assert result["ok"] is True
    assert runner.calls == [["scontrol", "update", "NodeName=worker1", "State=RESUME"]]


def test_arbitrary_command_tool_does_not_exist():
    runner = FakeRunner()
    from hpc_cluster_lab.slurm.runner import SlurmController

    registry = ToolRegistry(SlurmController(runner))
    result = registry.execute("run_command", {"command": "id", "node_name": "worker1"})
    assert result["ok"] is False
    assert runner.calls == []
