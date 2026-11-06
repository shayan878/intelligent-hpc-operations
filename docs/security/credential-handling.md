# Credential handling

The provided prototype contained an API token inline in Python source, while the accounting notes included a database password. These values are not repeated or packaged here.

Treat any credential pasted into a ticket, chat, source file, screenshot or public repository as exposed:

1. Revoke or rotate it at the issuing service immediately.
2. Remove it from the source and configuration history; if it was ever committed, rewriting the current file is not enough.
3. Inspect forks, build logs, artifacts, caches and shell history where applicable.
4. Store replacement secrets in a secret manager or protected environment variable.
5. Use `.env` only for local development, keep it ignored by Git, and never include it in logs or screenshots.

The assistant reads `LLM_API_KEY` from the environment and does not print it. Database secrets belong in the private `slurmdbd.conf` on the accounting host, with restrictive ownership and mode.
