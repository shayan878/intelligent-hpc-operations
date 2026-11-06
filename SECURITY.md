# Security policy

This repository contains infrastructure examples. They are not a substitute for a security review of your cluster.

## Reporting a vulnerability

Do not publish live credentials or exploit details in a public issue. Contact the repository maintainer privately through GitHub's security advisory feature.

## Security principles

- Keep API keys, passwords, private keys, MUNGE key material and host-specific secrets outside Git.
- Use dedicated service accounts and least-privilege permissions.
- Restrict NFS exports to trusted clients; retain `root_squash` unless a reviewed requirement says otherwise.
- Restrict Slurm controller and database ports to the cluster management network.
- Do not expose an unauthenticated LLM endpoint or cluster administration interface to an untrusted network.
- The assistant must not execute model-supplied shell strings. Administrative tools must be fixed, validated and approval-gated.
- Review all configuration examples for your exact Slurm and Linux versions before deployment.
