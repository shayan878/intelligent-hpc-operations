#!/usr/bin/env bash
#SBATCH --job-name=prime-multi
#SBATCH --output=prime-multi-%j-%t.out
#SBATCH --error=prime-multi-%j-%t.err
#SBATCH --nodes=2
#SBATCH --ntasks=2
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=400M
#SBATCH --time=00:10:00
#SBATCH --partition=batch

set -Eeuo pipefail

# Each task computes a unique interval based on SLURM_PROCID / SLURM_NTASKS.
srun --ntasks="${SLURM_NTASKS}" python3 -m intelligent_hpc_operations.workloads.primes --start 1 --end 100000
