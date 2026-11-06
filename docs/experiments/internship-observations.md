# Internship observations (source-grounded)

This page summarises the material provided for the project. It distinguishes recorded observations from configuration advice added during repository engineering. The notes did not include complete version, hardware, IP, screenshot or log data for every experiment.

## Day 2: NFS, Slurm and basic jobs

- Installed an NFS server on the controller and NFS clients on two workers.
- Mounted a shared home directory on workers and added a persistent mount entry.
- Installed Slurm Workload Manager on controller/workers.
- Built a `slurm.conf` with a controller, two workers, MUNGE authentication, a backfill scheduler and a debug partition.
- Recorded node resources as one CPU and 1200 MiB RAM in the example configuration.
- Wrote a prime-number Python script and submitted it using `sbatch`.
- Created a second job that split work across two Slurm tasks.

The original two-task Bash example placed a `RANGES` array in the parent script and referenced it inside a child `bash -c`. Shell arrays are not exported to child processes by default. The distributed Python example here calculates each rank's range from `SLURM_PROCID` and `SLURM_NTASKS`, avoiding that shell-scope dependency.

## Day 3: cgroups and preemption

- Changed Slurm process tracking/task plugins to cgroup-based plugins.
- Configured CPU, RAM and swap constraints.
- Created `batch` and `urgent` partitions with different `PriorityTier` values.
- Configured partition-priority preemption and `REQUEUE` mode.
- Reported an out-of-memory event from an intentionally unbounded memory-allocation test.

The repository does not include an unbounded memory-leak job. Use a bounded, controlled allocation test on an isolated worker. The supplied cgroup settings and kernel workaround were specific to the historical environment; use the current cgroup v2 guidance in this repository instead of copying legacy settings without validation.

## Day 4: accounting and operations

- Installed MariaDB and SlurmDBD and configured a Slurm accounting database.
- Created local users on controller/workers and aligned numeric UIDs/GIDs.
- Exported a shared directory and submitted multiple jobs under different users.
- Drained a worker for testing and observed new jobs running on the other worker; later resumed the drained node.
- Used `sinfo`, `squeue`, `sacct`, `scontrol` and `journalctl` for monitoring.
- Described an LLM-powered admin bot with tools for cluster status, job queue, node drain and running commands on a node.

The original material included an API credential and a database password. Both are intentionally excluded. Revoke/rotate them if they were ever valid.

## What is not claimed

- No claim that the source configurations are production safe.
- No claim that the cluster used modern cgroup v2; the notes include a legacy hierarchy change for one Slurm/OS combination.
- No claim that the two-worker job demonstrated MPI-based parallel computation; the provided example launched two independent Slurm tasks over separate input ranges.
- No claim that the original assistant safely constrained arbitrary commands; this repository replaces that interface with fixed, typed tools and explicit approval.
