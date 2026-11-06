from hpc_cluster_lab.assistant.bot import HPCAdminBot
from hpc_cluster_lab.assistant.registry import ToolRegistry
from hpc_cluster_lab.slurm.runner import CommandResult, SlurmController


class FakeRunner:
    def run(self, argv, timeout_seconds=20.0):
        return CommandResult(tuple(argv), 0, "worker1|idle", "")


class FakeClient:
    def __init__(self):
        self.responses = [
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": "call-1",
                        "type": "function",
                        "function": {"name": "get_cluster_status", "arguments": "{}"},
                    }
                ],
            },
            {"role": "assistant", "content": "worker1 is idle."},
        ]
        self.seen_messages = []

    def complete(self, messages, tools):
        self.seen_messages.append((list(messages), list(tools)))
        return self.responses.pop(0)


def test_bot_executes_read_only_tool_and_returns_final_message():
    client = FakeClient()
    registry = ToolRegistry(SlurmController(FakeRunner()))
    bot = HPCAdminBot(client, registry)
    assert bot.chat("What is the cluster status?") == "worker1 is idle."
    assert any(message["role"] == "tool" for message in bot.history)
    assert "drain_node" not in [x["function"]["name"] for x in client.seen_messages[0][1]]
