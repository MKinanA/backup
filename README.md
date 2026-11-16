# Simple Backup Tool for Linux

**IN DEVELOPMENT**

---

- `$ python -m backup --help`
  ```
  usage: python -m backup [-h] {list,create,info,modify,validate,run,check,schedule,delete} ...

  Simple backup tool for Linux.

  positional arguments:
    {list,create,info,modify,validate,run,check,schedule,delete}
      list                List created backup profiles.
      create              Create a new backup profile.
      info                Check the information (fields) of a backup profile.
      modify              Modify an existing backup profile.
      validate            Validate a backup profile, such as checking the provided paths.
      run                 Run a backup profile, creating an archive of the source file/directory and storing it in the backup directory.
      check               Check the backup archives stored in the backup path of a backup profile using their checksums for integrity.
      schedule            Schedule a backup profile to run automatically.
      delete              Delete a backup profile.

  options:
    -h, --help            show this help message and exit
  ```
<!--
---

## Known Edge Cases

- ### Two backup runs within the same second might overlap on the same backup archive file.
  Backup archive files are named with a timestamp down to the second. If two backup runs are initiated within the same second, they may attempt to write to the same archive file, which is not what you might want to happen. **The program DOES NOT check nor warn about this**.

- ### Backup destination inside the source directory can cause recursive backups.
  If the backup destination path is located inside the source directory, the backup process might include its own partial backup archive file in the backup itself. **The program DOES NOT check nor warn about this**.-->

---

## Quickstart

  ### 1. Dependencies
  Make sure your environment has these installed:
  - Python >=3.12
  - A cron implementation for your distro (e.g. `cron` for Debian/Ubuntu, `cronie` for Arch, etc.)
  - Python packages inside `requirements.txt`

  ### 2. Clone the repository, create a virtual environment (optional), and install dependencies
  `cd` into the directory you want, run `git clone https://github.com/MKinanA/backup.git`, and `cd` into the cloned repository. Optionally, create a python virtual environment and activate it (`python3 -m venv venv && source venv/bin/activate`). Install the dependencies with `pip install -r requirements.txt`.

  ### 3. Create a backup profile
  You need a name, source path, and backup path for the backup profile. Name is what you call and reference the profile by, source path is the directory or file you want to back up, and backup path is where you want to store the backup. Run `python3 -m backup create <name> <source_path> <backup_path>` to create the profile (e.g. `python3 -m backup create my_backup ~/Documents ~/Backups`). Check your created profiles with `python3 -m backup list` and check the profile's fields with `python3 -m backup info <name>`. Validate the profile with `python3 -m backup validate <name>` to ensure the paths are valid. If you want to modify the profile, run `python3 -m backup modify <name>` using the `--source` option to edit the source path and/or the `--backup` option to edit the backup path (e.g. `python3 -m backup modify my_backup --source ~/NewDocuments --backup ~/NewBackups`).

  ### 4. Run the backup profile manually
  Run `python3 -m backup run <name>` to run the backup profile. The backup will be created in the backup path you specified in the profile. You can check the backup archive file in the backup path. The backup archive file is named with the profile name, a timestamp, and the file's SHA-256 checksum, using the `.tar.gz` extension (e.g. `my_backup 2023-01-01-12-00-00 abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890.tar.gz`).

  ### 5. Schedule the backup profile to run automatically
  Run `python3 -m backup schedule <name> --set <cron_expression>` to schedule the backup profile (e.g. `python3 -m backup schedule my_backup --set "* * * * *"` for every minute). A cron job will be created for the profile. Ensure your cron service is running. Run `python3 -m backup schedule <name>` to check the schedule you've set for the profile. Check `cron.log` (in the repository root) for logs and your backup path for the automatically created backup archives. To unschedule the profile (remove the cron job), run `python3 -m backup schedule <name> --set remove`.

  ### 6. Check the integrity of the backup archives
  Run `python3 -m backup check <name>` to check the integrity of the backup archives stored in the backup path of the profile using their checksums (e.g. `python3 -m backup check my_backup`). The program will only check files in the directory that it recognizes by its filename (backup archives created automatically that you don't rename should pass the check) and ignore everything else.

  ### 7. Delete a backup profile
  Run `python3 -m backup delete <name>` to delete the backup profile (e.g. `python3 -m backup delete my_backup`). This will remove the saved profile, but it will not delete the backup archives stored in the backup path. Make sure to unschedule the profile first before deleting it.