from os import open as osopen, O_CREAT
from fcntl import flock, LOCK_EX, LOCK_UN
from contextlib import contextmanager
from pathlib import Path

@contextmanager
def open_file_with_lock(path: str | Path):
    with open(path, 'r+', opener=lambda path, flags: osopen(path, flags | O_CREAT)) as file:
        flock(file, LOCK_EX)
        try: yield file
        finally:
            file.flush()
            flock(file, LOCK_UN)