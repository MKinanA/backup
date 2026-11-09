from fcntl import flock, LOCK_EX, LOCK_UN
from contextlib import contextmanager
from pathlib import Path

@contextmanager
def open_file_with_lock(path: str | Path):
    file = open(path, 'r+')
    flock(file, LOCK_EX)
    try: yield file
    finally:
        flock(file, LOCK_UN)
        file.close()