#!/usr/bin/env bash
#SBATCH --job-name=short-queue-demo
#SBATCH --output=queue-%j.out
#SBATCH --error=queue-%j.err
#SBATCH --partition=batch
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=128M
#SBATCH --time=00:02:00

set -Eeuo pipefail
printf 'job=%s host=%s start=%s\n' "$SLURM_JOB_ID" "$(hostname)" "$(date -Is)"
sleep "$((15 + RANDOM % 20))"
printf 'job=%s finished=%s\n' "$SLURM_JOB_ID" "$(date -Is)"
