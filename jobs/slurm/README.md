# Slurm job examples

Install this Python package on the controller/worker execution environment (or make it available through a shared virtual environment) before submitting the prime jobs:

```bash
python3 -m pip install .
```

Examples:

- `prime-single.sbatch`: one task computes a complete range.
- `prime-distributed.sbatch`: two Slurm tasks compute disjoint subranges.
- `preemptible-batch.sbatch`: a short requeue-eligible job for a controlled partition-priority demonstration.
- `urgent-short.sbatch`: a short task submitted to the higher-tier partition.
- `short-cpu-load.sbatch`: finite queue-observation jobs; no unbounded memory or CPU load.

Never test preemption or resource limits on a shared production partition without administrator approval.
