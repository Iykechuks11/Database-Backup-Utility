# Database Backup Utility

Project inspiration from [roadmaps](https://roadmap.sh/projects/database-backup-utility)

- Step 1
    - Established connection with a docker postgres image. 
check

`python app/cli.py check --host 127.0.0.1 --port 5432 --user postgres --password mypass --dbname postgres`

- Step 2

- Step 3

- Step 4: Implementing the "Backup" (The Heavy Lifting)
backup

`python app/cli.py backup --user postgres --password mypass --dbname postgres --output my_first_backup.dump`

The first steps was to ensure a successhandshake between the cli too and the db engine.

- Step 5: Timestamps & Compression
We are going to upgrade the backup command to do three things:
    - <b>Unique Naming</b>: Automatically name the file backup_postgres_2026-03-09_02-15.sql.gz.

    - <b>Compression</b>: Use Python's gzip module to shrink the file size immediately.

    - <b>Path Management</b>: Ensure we have a dedicated backups/ folder so your root directory stays clean.
