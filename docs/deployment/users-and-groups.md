# Users, groups and shared identities

The internship notes created test users on the controller and workers with matching numeric UIDs/GIDs so that shared NFS files had consistent ownership. This is a key distributed-filesystem requirement: Linux file ownership on NFS is based on numeric identities, not simply the displayed username.

## Small-lab procedure

1. Decide the UID/GID mapping centrally before creating accounts.
2. Create the same numeric UID and primary GID on every node, or use a central identity service.
3. Create project directories with a project group and deliberate permissions.
4. Verify ownership from the controller and every worker.
5. Test as a non-privileged user before submitting jobs.

Example checks:

```bash
id username
getent passwd username
getent group project-group
stat -c '%u:%g %a %n' /srv/hpc/shared/project
```

Do not use `chmod 777` to paper over mismatched IDs. Do not place user passwords or authentication hashes in this repository. For production, use LDAP, FreeIPA, Active Directory integration, SSSD or another managed identity source rather than maintaining local accounts manually.
