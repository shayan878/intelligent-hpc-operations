# Contributing

Thanks for helping improve the Slurm HPC Cluster Lab.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
ruff check .
pytest -q
```

## Contribution guidelines

- Keep examples safe to run on shared infrastructure. Do not add unbounded memory/CPU loops or destructive cluster commands as default examples.
- Never commit credentials, private keys, database dumps, host-specific IP addresses, internal domains or real user data.
- Keep the assistant's tool interface typed and allow-listed. Do not add arbitrary shell execution or `shell=True`.
- Mutating cluster operations must remain opt-in and require explicit operator confirmation.
- Document the Slurm release, Linux distribution and relevant kernel/systemd assumptions for configuration changes.
- Add tests for Python behavior and provide a clear manual validation procedure for cluster-specific behavior.
- Do not claim that a command or configuration was tested on a real cluster unless the test was actually performed.

Open an issue before introducing a substantial new capability. Pull requests should include the motivation, risks, test evidence and documentation updates.
