# Partitions and preemption

The internship lab created `batch` and `urgent` partitions on the same workers and assigned the urgent partition a higher priority tier.

## Example policy

```ini
PriorityType=priority/multifactor
PreemptType=preempt/partition_prio
PreemptMode=REQUEUE
JobRequeue=1

PartitionName=batch  Nodes=worker[1-2] Default=YES MaxTime=INFINITE State=UP PriorityTier=1
PartitionName=urgent Nodes=worker[1-2]              MaxTime=01:00:00 State=UP PriorityTier=2
```

A larger `PriorityTier` is considered ahead of lower-tier partitions and can make those lower-tier jobs eligible for preemption when `PreemptType=preempt/partition_prio` is active. [Slurm preemption guide](https://slurm.schedmd.com/preempt.html).

With `PreemptMode=REQUEUE`, a preempted job is requeued only when it is eligible for requeue: use `#SBATCH --requeue` or set the cluster-wide `JobRequeue=1`. [Slurm `slurm.conf` reference](https://slurm.schedmd.com/slurm.conf.html).

## Example jobs

- [`preemptible-batch.sbatch`](../../jobs/slurm/preemptible-batch.sbatch) submits a restartable lower-priority workload.
- [`urgent-short.sbatch`](../../jobs/slurm/urgent-short.sbatch) submits to the higher-tier partition.

## Operational considerations

- Requeue does not magically checkpoint application state. A job must safely restart or implement its own checkpointing.
- Do not test preemption on other users' jobs or production partitions.
- Use a maintenance/test partition and a short time limit.
- Observe `squeue`, `scontrol show job JOB_ID` and `sacct` before, during and after the test.
- Equal `PriorityTier` values do not provide the tier-based preemption relation shown here.
- Preemption policy interacts with QOS, reservations, job priority and partition overlap; review the official guide before production use.
