from os import open as osopen, O_CREAT, fsync
from fcntl import flock, LOCK_EX, LOCK_UN, LOCK_SH
from contextlib import contextmanager
from pathlib import Path

@contextmanager
def open_file_with_lock(path: str | Path, shared_readonly: bool = False):
    with open(path, 'r' if shared_readonly else 'r+', opener=lambda path, flags: osopen(path, flags | O_CREAT)) as file:
        flock(file, LOCK_SH if shared_readonly else LOCK_EX)
        try: yield file
        finally:
            file.flush()
            fsync(file.fileno())
            flock(file, LOCK_UN)