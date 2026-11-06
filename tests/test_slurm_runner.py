import pytest

from hpc_cluster_lab.slurm.runner import CommandResult, SlurmController


class FakeRunner:
    def __init__(self):
        self.calls = []

    def run(self, argv, timeout_seconds=20.0):
        self.calls.append(argv)
        return CommandResult(tuple(argv), 0, "ok", "")


def test_read_only_status_commands_are_fixed():
    runner = FakeRunner()
    controller = SlurmController(runner=runner, allowed_nodes=("worker1",))
    controller.get_cluster_status()
    controller.get_active_jobs()
    controller.get_job_details("123")
    assert runner.calls[0][0] == "sinfo"
    assert runner.calls[1][0] == "squeue"
    assert runner.calls[2] == ["scontrol", "show", "job", "123"]


def test_job_id_is_validated_before_command():
    runner = FakeRunner()
    controller = SlurmController(runner=runner)
    with pytest.raises(ValueError):
        controller.get_job_details("123;whoami")
    assert runner.calls == []


def test_admin_nodes_must_be_allow_listed():
    runner = FakeRunner()
    controller = SlurmController(runner=runner, allowed_nodes=("worker1",))
    with pytest.raises(PermissionError):
        controller.drain_node("controller")
    assert runner.calls == []


def test_admin_commands_are_argument_arrays():
    runner = FakeRunner()
    controller = SlurmController(runner=runner, allowed_nodes=("worker1",))
    controller.drain_node("worker1")
    controller.resume_node("worker1")
    assert runner.calls[0] == [
        "scontrol",
        "update",
        "NodeName=worker1",
        "State=DRAIN",
        "Reason=OperatorApprovedMaintenance",
    ]
    assert runner.calls[1] == ["scontrol", "update", "NodeName=worker1", "State=RESUME"]
