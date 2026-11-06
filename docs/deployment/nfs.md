# NFS shared storage

This guide captures the controller-as-NFS-server and worker-as-NFS-client pattern from the internship notes, with safer defaults.

## Controller: install and export

```bash
sudo apt update
sudo apt install nfs-kernel-server
sudo mkdir -p /srv/hpc/shared
sudo chown root:root /srv/hpc/shared
sudo chmod 0755 /srv/hpc/shared
```

Review [`configs/nfs/exports.example`](../../configs/nfs/exports.example). Replace the documentation-only subnet with the smallest trusted cluster subnet, then install the line in `/etc/exports`:

```text
/srv/hpc/shared 192.0.2.0/24(rw,sync,no_subtree_check,root_squash)
```

Apply and inspect the export:

```bash
sudo exportfs -rav
sudo exportfs -v
sudo systemctl enable --now nfs-kernel-server
```

Do not export to `*` unless the access model has been deliberately reviewed. Ubuntu's guide recommends using a specific client/hostname declaration; `no_root_squash` allows remote root to act as root on the export and can create security problems. [Ubuntu NFS guide](https://ubuntu.com/server/docs/how-to/networking/install-nfs/).

## Workers: install and mount

On each worker:

```bash
sudo apt update
sudo apt install nfs-common
sudo mkdir -p /srv/hpc/shared
sudo mount controller:/srv/hpc/shared /srv/hpc/shared
findmnt /srv/hpc/shared
df -h /srv/hpc/shared
```

For a persistent systemd-managed mount, adapt [`configs/nfs/fstab.example`](../../configs/nfs/fstab.example), then:

```bash
sudo systemctl daemon-reload
sudo mount -a
findmnt /srv/hpc/shared
```

## Permissions and identity

- Keep UID/GID values consistent across nodes; prefer a central identity source as the cluster grows.
- Use project/group directories with deliberate ownership and `setgid` where shared group inheritance is required.
- Avoid `chmod 777` as a general fix. Diagnose ownership and group membership instead.
- Keep root squashing enabled unless a narrow, reviewed diskless-client requirement applies.
- Consider Kerberos-backed NFS (`sec=krb5i` or `sec=krb5p`) where your threat model requires authenticated/integrity-protected/encrypted NFS traffic.

## Validation checklist

- [ ] Only intended worker addresses can mount the share.
- [ ] A normal user can write only to intended project paths.
- [ ] UID/GID ownership appears consistently on controller and workers.
- [ ] The mount survives reboot and network restart as expected.
- [ ] Worker jobs can read input and write output without relying on world-writable permissions.
