#!/usr/bin/env bash
set -Eeuo pipefail

CONFIG="${1:-configs/slurm/slurm.conf.example}"
if [[ ! -r "$CONFIG" ]]; then
    echo "Cannot read Slurm config: $CONFIG" >&2
    exit 2
fi

# This is a lightweight preflight, not a Slurm parser. The authoritative check
# is to run the matching Slurm release in a disposable test environment.
for key in ClusterName SlurmctldHost AuthType StateSaveLocation SlurmdSpoolDir SchedulerType SelectType NodeName PartitionName; do
    if ! grep -Eq "^[[:space:]]*${key}=" "$CONFIG"; then
        echo "Missing expected setting: ${key}" >&2
        exit 1
    fi
done

if grep -Eq 'REPLACE_WITH|CHANGE_ME|192\.0\.2\.' "$CONFIG"; then
    echo "Template placeholders remain. Replace them before deployment." >&2
    exit 1
fi

echo "Basic configuration preflight passed for ${CONFIG}."
echo "This does not validate plugin availability or Slurm syntax; test with your installed Slurm version."
