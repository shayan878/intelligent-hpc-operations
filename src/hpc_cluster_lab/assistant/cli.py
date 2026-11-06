"""Interactive entry point for the optional HPC cluster assistant."""

from __future__ import annotations

import argparse
import sys

from hpc_cluster_lab.assistant.api_client import OpenAICompatibleClient
from hpc_cluster_lab.assistant.bot import HPCAdminBot
from hpc_cluster_lab.assistant.config import Settings
from hpc_cluster_lab.assistant.registry import ToolRegistry
from hpc_cluster_lab.slurm.runner import SlurmController


def _confirm(prompt: str) -> bool:
    print(f"\nADMIN ACTION: {prompt}")
    print("This operation changes Slurm node state.")
    return input("Type 'yes' to approve: ").strip().lower() == "yes"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Chat with a guarded Slurm cluster assistant")
    parser.add_argument(
        "--enable-admin-actions",
        action="store_true",
        help="Expose drain/resume tools; each operation still requires terminal approval",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        settings = Settings.from_env()
    except ValueError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2

    if args.enable_admin_actions and not settings.allowed_nodes:
        print(
            "Refusing to enable administrative tools without SLURM_ALLOWED_NODES.",
            file=sys.stderr,
        )
        return 2

    controller = SlurmController(allowed_nodes=settings.allowed_nodes)
    registry = ToolRegistry(
        controller,
        include_admin=args.enable_admin_actions,
        approval_callback=_confirm if args.enable_admin_actions else None,
    )

    try:
        with OpenAICompatibleClient(settings) as client:
            bot = HPCAdminBot(client, registry, max_tool_rounds=settings.max_tool_rounds)
            print("Slurm HPC Assistant | read-only by default | type 'exit' to quit")
            if args.enable_admin_actions:
                print("Administrative tools enabled; every change requires terminal approval.")
            while True:
                try:
                    message = input("\nYou: ").strip()
                except (EOFError, KeyboardInterrupt):
                    print("\nExiting.")
                    break
                if message.lower() in {"exit", "quit"}:
                    break
                if not message:
                    continue
                try:
                    print(f"\nAssistant: {bot.chat(message)}")
                except Exception as exc:  # Keep interactive session alive on a request failure.
                    print(f"Request failed: {exc}", file=sys.stderr)
    except KeyboardInterrupt:
        print("\nExiting.")
    return 0
