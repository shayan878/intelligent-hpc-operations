# Job examples

## Single-node job

```bash
sbatch jobs/slurm/prime-single.sbatch
```

## Two-task job

```bash
sbatch jobs/slurm/prime-distributed.sbatch
```

The Python worker assigns each task a distinct half-open integer interval. `SLURM_PROCID` is the task rank and `SLURM_NTASKS` is the task count (see [Slurm `srun`](https://slurm.schedmd.com/srun.html)). Each task prints its assigned interval and prime count. This example demonstrates Slurm task distribution, not MPI communication.

## Scheduler stress without a memory leak

```bash
for i in {1..4}; do sbatch jobs/slurm/short-cpu-load.sbatch; done
```

This submits short bounded sleep jobs. Use it to observe queue state and worker allocation; it is not a benchmark of CPU throughput.
