#!/usr/bin/env bash
#SBATCH --job-name=prime-single
#SBATCH --output=prime-single-%j.out
#SBATCH --error=prime-single-%j.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=500M
#SBATCH --time=00:10:00
#SBATCH --partition=batch

set -Eeuo pipefail

python3 -m intelligent_hpc_operations.workloads.primes --start 1 --end 100000
