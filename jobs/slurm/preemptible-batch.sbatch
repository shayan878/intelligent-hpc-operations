#!/usr/bin/env bash
#SBATCH --job-name=batch-requeue-demo
#SBATCH --output=batch-requeue-%j.out
#SBATCH --error=batch-requeue-%j.err
#SBATCH --partition=batch
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=256M
#SBATCH --time=00:10:00
#SBATCH --requeue

set -Eeuo pipefail

# Short, restartable demonstration only. Real jobs should checkpoint their state.
for step in {1..6}; do
    echo "checkpoint-like progress marker: step=${step} time=$(date -Is)"
    sleep 10
done
