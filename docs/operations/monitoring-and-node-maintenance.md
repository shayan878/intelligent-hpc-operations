# Monitoring and node maintenance

## Read-only monitoring commands

```bash
sinfo -Nel
squeue -o "%.18i %.12P %.20j %.10u %.2t %.10M %.6D %R"
scontrol show nodes
scontrol show job JOB_ID
sacct -j JOB_ID --format=JobID,User,State,Elapsed,AllocCPUS,NodeList
systemctl status slurmctld   # controller
systemctl status slurmd      # worker
journalctl -u slurmctld -n 50 --no-pager
journalctl -u slurmd -n 50 --no-pager
```

See [`scripts/cluster-health.sh`](../../scripts/cluster-health.sh) for a compact read-only report.

## Drain and resume

Drain a node before planned maintenance so new jobs are not assigned to it:

```bash
sudo scontrol update NodeName=worker1 State=DRAIN Reason="planned maintenance"
```

After maintenance, return it to service:

```bash
sudo scontrol update NodeName=worker1 State=RESUME
```

Inspect the node and its jobs before changing state. A drain request does not necessarily terminate jobs already running on that node. Do not use `State=IDLE` as a shortcut to override a reason or diagnose the underlying issue; `RESUME` is the intended administrative transition after the cause has been addressed.

## Troubleshooting order

1. `scontrol ping` and `systemctl status` for controller/worker daemons.
2. Compare Slurm configuration checksums across all nodes.
3. Verify MUNGE is active and clocks are synchronised.
4. Check node resource definitions against `slurmd -C`.
5. Inspect service logs before changing cgroup, MPI or plugin settings.
6. Verify NFS is mounted and users have aligned IDs and intended permissions.
7. Review `sinfo`, `squeue`, `scontrol show node` and `sacct` state.

Avoid deleting `/var/spool/slurmd` or controller state as a generic restart fix. Back up first and follow a documented recovery plan.
