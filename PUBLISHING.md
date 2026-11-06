# Publish this repository to GitHub

## Recommended metadata

- **Repository:** `slurm-hpc-cluster-lab`
- **Description:** `A hands-on Slurm HPC cluster lab: NFS shared storage, cgroup resource controls, partition preemption, accounting, multi-node workloads, and a guarded LLM operations assistant.`
- **Visibility:** Public only after publication permission and credential rotation are confirmed.
- **Topics:** `slurm`, `hpc`, `workload-manager`, `distributed-computing`, `nfs`, `cgroups`, `linux`, `python`, `llm`, `cluster-management`, `job-scheduler`, `ai-ops`.

## Create the empty repository

On GitHub, choose **New repository**, use the name above, and do not initialise it with a README, `.gitignore` or license. This archive already contains project files.

## Push with GitHub CLI

Extract the ZIP, open a terminal in the extracted `slurm-hpc-cluster-lab` directory, and run:

```bash
gh auth login
git init -b main
git add .
git status --short
# Inspect the staged file list before committing.
git commit -m "Initial commit: Slurm HPC cluster lab"
gh repo create slurm-hpc-cluster-lab \
  --public \
  --description "A hands-on Slurm HPC cluster lab: NFS, cgroups, preemption, accounting, multi-node jobs and a guarded LLM assistant." \
  --source=. \
  --remote=origin \
  --push
```

If you created the empty repository in the browser instead, add its remote and push:

```bash
git remote add origin https://github.com/shayan878/slurm-hpc-cluster-lab.git
git push -u origin main
```

## Set repository topics

```bash
gh repo edit shayan878/slurm-hpc-cluster-lab \
  --add-topic slurm \
  --add-topic hpc \
  --add-topic workload-manager \
  --add-topic distributed-computing \
  --add-topic nfs \
  --add-topic cgroups \
  --add-topic linux \
  --add-topic python \
  --add-topic llm \
  --add-topic cluster-management \
  --add-topic job-scheduler \
  --add-topic ai-ops
```

Then enable Issues and Discussions if you plan to maintain the project, confirm GitHub Actions succeeds, and pin the repository on your profile.

## Before making it public

- Rotate/revoke the LLM API credential and database password that appeared in the supplied source material.
- Confirm permission to publish the collaborative internship material and its attribution.
- Keep private `.env`, SlurmDBD config, MUNGE key files, host-specific addresses, screenshots and job outputs out of the commit.
- Do not add an open-source license until rights holders agree; see [`LICENSE_STATUS.md`](LICENSE_STATUS.md).
- Read the staged file list carefully before pushing.
