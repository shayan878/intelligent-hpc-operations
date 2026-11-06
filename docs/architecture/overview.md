# Cluster architecture

## Roles

| Role | Responsibilities | Typical services |
|---|---|---|
| Controller | Scheduling, cluster state, job accounting integration, shared home/project management | `slurmctld`, optional `slurmdbd`, MariaDB, NFS server, MUNGE |
| Worker | Executes allocated jobs and enforces job resource limits | `slurmd`, MUNGE, cgroup controllers, NFS client |
| Operator workstation | Submits jobs, inspects state and optionally uses the guarded assistant | Slurm client commands, Python package |

## Control plane and data plane

The Slurm controller makes scheduling decisions and coordinates worker daemons. NFS is a shared filesystem service, not the scheduler. SlurmDBD records accounting data in a database; it is not needed for basic `sbatch`/`srun` scheduling but is needed for the accounting workflow described here.

## Identity is part of the architecture

NFS file ownership is numeric. Users and groups that need consistent ownership across workers should have aligned UID/GID values, normally backed by LDAP/FreeIPA/SSSD or another central identity service in a larger environment. The internship notes created matching local IDs manually; that is acceptable only for a controlled small lab and is easy to drift.

## Network boundaries

Use a dedicated management/cluster network where possible. Restrict NFS, MUNGE, Slurm controller/worker, database and LLM endpoint traffic with host/network firewalls. Do not publish private cluster addresses in the public repository.

## Architecture artwork

The README embeds [`../../assets/cluster-architecture.svg`](../../assets/cluster-architecture.svg). Edit the SVG if the actual lab topology differs.
