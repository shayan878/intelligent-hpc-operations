# Slurm controller and worker setup

This is a manual deployment guide for a small lab. Commands vary by distribution and package version; pin and test the same Slurm release on all hosts.

## 1. Establish prerequisites

- Stable DNS or `/etc/hosts` entries for `controller`, `worker1`, `worker2`.
- Consistent time synchronization.
- Identical Slurm/MUNGE package versions and compatible plugin paths.
- A shared MUNGE key distributed securely to all participating nodes; never commit it.
- Consistent Slurm user/group identity and filesystem permissions.
- Firewall rules allowing only the cluster nodes to communicate with required Slurm/NFS/database ports.

## 2. Install packages

On the controller and each worker, install the Slurm workload-manager packages and MUNGE using the distribution's supported packages. On Debian/Ubuntu family systems the internship used:

```bash
sudo apt update
sudo apt install slurm-wlm munge
```

The controller additionally needs the controller service; workers need the compute daemon. Package names and service names can differ by distribution.

## 3. Inspect worker resources

On each worker run:

```bash
sudo slurmd -C
```

Use the discovered CPU, socket/core/thread, memory and GRES information to define the node. Do not assume `CPUs=1 RealMemory=1200` from the historic lab applies to your system.

## 4. Configure Slurm

Start from [`slurm.conf.example`](../../configs/slurm/slurm.conf.example). Review the following fields carefully:

- `ControlMachine` and node names must resolve consistently.
- `StateSaveLocation` and `SlurmdSpoolDir` must exist and have correct ownership.
- `ProctrackType` and `TaskPlugin` must match installed plugins.
- `SelectType=select/cons_tres` is required for the resource accounting pattern shown.
- `AccountingStorageType=accounting_storage/slurmdbd` should be enabled only after SlurmDBD is configured and reachable.
- The `urgent` partition's higher `PriorityTier` enables the partition-priority preemption policy when `PreemptType=preempt/partition_prio` is selected.

Copy the same validated configuration to every Slurm node. Compare checksums:

```bash
sha256sum /etc/slurm/slurm.conf
```

Prefer config management over manual SCP when the cluster grows.

## 5. Prepare state directories

Example only; verify the service account and paths for your distribution:

```bash
sudo install -d -o slurm -g slurm -m 0755 /var/spool/slurmctld
sudo install -d -o root -g root -m 0755 /var/spool/slurmd
sudo install -d -o slurm -g slurm -m 0755 /var/log/slurm
```

`StateSaveLocation` must be writable by `SlurmUser`; `SlurmdSpoolDir` is a worker-local directory accessible to root and should not be placed on the shared NFS mount. Check the file-permission requirements in the official [`slurm.conf` reference](https://slurm.schedmd.com/slurm.conf.html).

## 6. Start services in order

Start MUNGE on all nodes, then the controller and worker daemons according to your distribution's service units:

```bash
sudo systemctl enable --now munge
sudo systemctl enable --now slurmctld   # controller only
sudo systemctl enable --now slurmd      # workers only
```

Validate:

```bash
sinfo -Nel
scontrol ping
scontrol show nodes
```

Use `journalctl -u slurmctld` on the controller and `journalctl -u slurmd` on a worker to diagnose service startup issues.

## 7. Submit a controlled job

```bash
sbatch jobs/slurm/prime-single.sbatch
squeue
sacct -j JOB_ID --format=JobID,JobName,State,Elapsed,AllocCPUS,NodeList
```

Do not clear Slurm spool/state directories to troubleshoot a running cluster. Back up configuration and understand the state being removed before performing any destructive recovery operation.
