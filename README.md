# Simple Backup Tool for Linux

**IN DEVELOPMENT**

---

- `$ python -m backup --help`
  ```
  usage: python -m backup [-h] {list,create,info,validate,run,schedule,delete} ...

  Simple backup tool for Linux.

  positional arguments:
    {list,create,info,validate,run,schedule,delete}
      list                List created backup profiles.
      create              Create a new backup profile.
      info                Check the information (fields) of a backup profile.
      validate            Validate a backup profile, such as checking the provided paths.
      run                 Run a backup profile, creating an archive of the source file/directory and storing it in the backup directory.
      schedule            Schedule a backup profile to run automatically.
      delete              Delete a backup profile.

  options:
    -h, --help            show this help message and exit
  ```

---

## Known Edge Cases

- ### Two backup runs within the same second might overlap on the same backup archive file.
  Backup archive files are named with a timestamp down to the second. If two backup runs are initiated within the same second, they may attempt to write to the same archive file, which is not what you might want to happen. **The program DOES NOT check nor warn about this**.

- ### Backup destination inside the source directory can cause recursive backups.
  If the backup destination path is located inside the source directory, the backup process might include its own partial backup archive file in the backup itself. **The program DOES NOT check nor warn about this**.