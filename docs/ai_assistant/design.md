# LLM-powered HPC cluster assistant

The supplied project notes describe an assistant that talks to an OpenAI-compatible chat-completions endpoint and exposes Slurm tools. The prototype's concerns are separated into focused modules:

```text
ai_assistant/
├── config.py          # Environment-based settings; no committed credentials
├── api_client.py      # HTTP transport to an OpenAI-compatible endpoint
├── schemas.py         # Explicit function-tool JSON schemas
├── registry.py        # Tool dispatch, validation and approval gates
├── bot.py             # Conversation and tool-call loop
└── cli.py             # Interactive terminal entry point

slurm/runner.py        # Fixed argv-based Slurm commands (shell=False)
```

## Available tools

| Tool | Purpose | Permission |
|---|---|---|
| `get_cluster_status` | Read node and state summary (`sinfo`) | Read-only |
| `get_active_jobs` | Read active/pending job queue (`squeue`) | Read-only |
| `get_job_details` | Read one numeric job ID (`scontrol show job`) | Read-only |
| `drain_node` | Drain one allow-listed worker | Admin opt-in + terminal confirmation |
| `resume_node` | Resume one allow-listed worker | Admin opt-in + terminal confirmation |

The unrestricted `run_command(command, node_name)` function from the prototype is intentionally absent. Model-generated arguments are untrusted; a shell command interface would allow prompt injection to become command execution.

## Safety model

1. No API token or internal endpoint is hard-coded. Settings are read from environment variables.
2. The default tool list is read-only.
3. Administrative tools are only advertised when `--enable-admin-actions` is supplied.
4. Drain/resume targets must exactly match `SLURM_ALLOWED_NODES`.
5. Every administrative request needs an interactive `yes` confirmation from the operator.
6. Commands are built as argument arrays and executed without a shell.
7. The assistant runs with the current OS identity. Use a least-privilege Slurm account and do not run as root for convenience.
8. The tool loop has a finite maximum number of rounds.

These controls reduce risk but do not make an LLM a trusted administrator. Review every proposed action and retain normal Slurm permissions, logging and change-control practices.
