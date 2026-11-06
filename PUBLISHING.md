# Repository publishing and maintenance

This repository is already published as:

https://github.com/shayan878/intelligent-hpc-operations

## Recommended GitHub About metadata

**Description**

`An intelligent HPC operations toolkit featuring Slurm workload scheduling, distributed computing, resource isolation, NFS shared storage, accounting, and LLM-powered cluster administration.`

**Topics**

`hpc`, `slurm`, `cluster-management`, `distributed-systems`, `workload-scheduling`, `nfs`, `cgroups`, `python`, `llm`, `ai-operations`, `linux`, `automation`.

Set these in the repository's About panel using its settings icon. The GitHub connection used for repository code changes cannot edit repository description/topics directly.

## Branch protection

For a personal portfolio repository, protect `main` against accidental force-push and deletion. Recommended rules:

- Require a pull request before merging.
- Require the CI workflow to pass before merging.
- Block force pushes.
- Block branch deletion.

Enable these in **Settings → Rules → Rulesets** (or **Settings → Branches**, depending on the GitHub UI). Do not require an additional reviewer unless you have someone who can review your changes.

## Dependency updates

Dependabot is configured for GitHub Actions and Python dependencies. Review update PRs after the base branch CI is green. Merge only updates whose diff and workflow results you understand.

## Before a public announcement

- [ ] Confirm that the internship material may be published and attributed.
- [ ] Rotate any credentials that appeared in the original source material.
- [ ] Keep private `.env`, MUNGE keys, real SlurmDBD config and job outputs out of Git.
- [ ] Confirm that the README CI badge reflects the actual workflow result.
- [ ] Run the unit tests and config preflight locally.
- [ ] Add a real terminal demo only after validating the project on a cluster you control.
- [ ] Do not claim production-readiness or measured performance without reproducible evidence.

## Local maintenance commands

```bash
python -m pip install -e '.[dev]'
ruff check .
pytest -q
python -m compileall -q src tests
bash -n scripts/*.sh jobs/slurm/*.sbatch
bash scripts/validate-config.sh configs/slurm/slurm.conf.example
```

## Licensing

No open-source license is included until the collaborative internship source material's publication and licensing rights are confirmed. See [LICENSE_STATUS.md](LICENSE_STATUS.md).
