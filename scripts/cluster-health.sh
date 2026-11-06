#!/usr/bin/env bash
set -Eeuo pipefail

printf '
== Slurm controller ==
'
if command -v scontrol >/dev/null 2>&1; then
    scontrol ping || true
else
    echo "scontrol not found"
fi

printf '
== Nodes ==
'
if command -v sinfo >/dev/null 2>&1; then
    sinfo -Nel || true
else
    echo "sinfo not found"
fi

printf '
== Queue ==
'
if command -v squeue >/dev/null 2>&1; then
    squeue -o "%.18i %.12P %.18j %.10u %.2t %.10M %.6D %R" || true
else
    echo "squeue not found"
fi

printf '
== NFS shared mount ==
'
if mountpoint -q /srv/hpc/shared; then
    findmnt /srv/hpc/shared
else
    echo "/srv/hpc/shared is not mounted (edit this path for your site)"
fi
