# Slurm accounting with SlurmDBD

The internship notes used MariaDB, `slurmdbd`, a database named `slurm_acct_db`, and the `sacctmgr` command to register the cluster.

## 1. Create a database and restricted user

Use a dedicated password generated and stored in a secret manager or private root-readable file. Do not reuse a human password.

Illustrative SQL (replace the placeholder locally; do not commit the real value):

```sql
CREATE DATABASE slurm_acct_db;
CREATE USER 'slurm'@'localhost' IDENTIFIED BY 'REPLACE_WITH_PRIVATE_SECRET';
GRANT ALL PRIVILEGES ON slurm_acct_db.* TO 'slurm'@'localhost';
FLUSH PRIVILEGES;
```

Grant only the privileges required by the official deployment guide and your MariaDB/MySQL version. If the database is remote, scope the database account to the SlurmDBD host rather than `%`.

## 2. Configure SlurmDBD

Start from [`slurmdbd.conf.example`](../../configs/slurm/slurmdbd.conf.example). The file contains `StoragePass`, so it must be readable only by the service account/root and must not be tracked by Git:

```bash
sudo chown slurm:slurm /etc/slurm/slurmdbd.conf
sudo chmod 0600 /etc/slurm/slurmdbd.conf
```

SchedMD explicitly warns that `slurmdbd.conf` contains a database password and should be protected with restrictive permissions. [Reference](https://slurm.schedmd.com/slurmdbd.conf.html).

## 3. Enable accounting

After validating SlurmDBD, configure `AccountingStorageType=accounting_storage/slurmdbd` and `AccountingStorageHost` in `slurm.conf`. Start the database, then `slurmdbd`, then ensure `slurmctld` can connect.

Register the cluster using the correct name from `slurm.conf`:

```bash
sudo sacctmgr add cluster hpc-lab
sacctmgr show cluster
```

## 4. Useful reports

```bash
sacct -X --allusers --format=JobID,User,State,JobName%20,Start,Elapsed,AllocCPUS,NodeList
sacct -u "$USER" --format=JobID,JobName,State,Elapsed,MaxRSS,NodeList
squeue -o "%.18i %.12P %.20j %.10u %.2t %.10M %.6D %R"
```

`MaxRSS` availability and accounting granularity depend on `JobAcctGatherType`, frequency, cgroup support and Slurm version. Never publish real usernames, job arguments, filesystem paths or other potentially sensitive accounting data without redaction.
