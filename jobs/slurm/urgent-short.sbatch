#!/usr/bin/env bash
#SBATCH --job-name=urgent-demo
#SBATCH --output=urgent-%j.out
#SBATCH --error=urgent-%j.err
#SBATCH --partition=urgent
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=128M
#SBATCH --time=00:02:00

set -Eeuo pipefail
hostname
srun --ntasks=1 bash -c 'echo "urgent partition task on $(hostname)"; sleep 15'
