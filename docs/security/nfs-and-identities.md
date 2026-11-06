# NFS and identity security

- Restrict exports to named cluster hosts or a narrowly scoped subnet.
- Retain `root_squash`; Linux NFS maps remote UID/GID 0 to an anonymous identity by default. `no_root_squash` disables that protection. See [`exports(5)`](https://man7.org/linux/man-pages/man5/exports.5.html).
- Avoid permissive `chmod 777` workarounds. Create project groups and set ownership/mode intentionally.
- Keep UID/GID mappings consistent across all nodes; central identity management is preferable beyond a small lab.
- Protect MUNGE key material and distribute it through a secure channel.
- Restrict Slurm controller, worker, NFS and database ports to hosts that need them.
- Keep `/etc/slurm/slurmdbd.conf` private; it contains database authentication material and SchedMD recommends restrictive permissions.
