# cgroups and resource enforcement

The original lab enabled Slurm's `proctrack/cgroup` and `task/cgroup` plugins and constrained cores, RAM and swap. The repository template modernises this for cgroup v2-capable systems.

## Recommended starting point

Review [`configs/slurm/cgroup.conf.example`](../../configs/slurm/cgroup.conf.example) and the corresponding `slurm.conf` entries. SchedMD documents `CgroupPlugin=autodetect` and the common constraints `ConstrainCores`, `ConstrainRAMSpace`, `ConstrainSwapSpace` and `ConstrainDevices`. [cgroup.conf reference](https://slurm.schedmd.com/cgroup.conf.html).

Slurm supports cgroup v1 and v2, but cgroup v1 is deprecated and no new features are planned for it starting with Slurm 25.05. Hybrid v1/v2 mode is not supported. [Slurm cgroups guide](https://slurm.schedmd.com/cgroups.html).

## Key configuration

```ini
# slurm.conf
ProctrackType=proctrack/cgroup
TaskPlugin=task/cgroup,task/affinity
JobAcctGatherType=jobacct_gather/cgroup

# cgroup.conf
CgroupPlugin=autodetect
ConstrainCores=yes
ConstrainRAMSpace=yes
ConstrainSwapSpace=yes
AllowedRAMSpace=100
AllowedSwapSpace=0
```

`RealMemory` in `slurm.conf` should leave room for operating-system and daemon memory; it should not blindly equal the machine's entire physical RAM. Consult the Slurm cgroup guide for `MemSpecLimit`, task containment, device constraints and PAM integration.

## Validation

```bash
stat -fc %T /sys/fs/cgroup
cat /proc/self/cgroup
scontrol show config | grep -E 'ProctrackType|TaskPlugin|JobAcctGatherType'
```

A cgroup v2 filesystem normally reports `cgroup2fs`. Confirm the actual version and available controllers rather than applying a GRUB workaround copied from a different Linux/Slurm release. Restart Slurm daemons only during a planned maintenance window.

## Safe memory-limit experiment

Start with a bounded job that allocates a known, small amount of memory and requests a lower Slurm memory limit. Do not use an infinite memory leak on shared hardware. Verify the job's `State`, exit code and accounting fields with `sacct`; inspect cgroup counters on a worker only when you know the relevant path for your Slurm version.
