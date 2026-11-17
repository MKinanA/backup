from contextlib import contextmanager
from pathlib import Path
from json import loads as jsonloads, dumps as jsondumps, JSONDecodeError
from copy import deepcopy
from .open_file_with_lock import open_file_with_lock

DATABASE_PATH = (Path(__file__).parent.parent / 'database.json').resolve()
MAX_READ_ATTEMPTS = 2

def database_read() -> dict:
    attempts = 0
    exc = None
    while attempts < MAX_READ_ATTEMPTS:
        attempts += 1
        database_raw = None
        try:
            with open(DATABASE_PATH, 'r') as database_file: return jsonloads(database_raw := database_file.read())
        except (JSONDecodeError, FileNotFoundError) as e:
            exc = e
            if not database_raw:
                with database_write(): pass
            else: raise
    raise RuntimeError('Failed to parse database.') from exc

@contextmanager
def database_write():
    force_write_anyway = False
    with open_file_with_lock(DATABASE_PATH) as database_file:
        database_dict = {}
        try: database_dict = jsonloads(database_raw := database_file.read())
        except JSONDecodeError:
            if database_raw: raise
            else: force_write_anyway = True
        original = deepcopy(database_dict)
        try: yield database_dict
        except: raise
        else:
            if (database_dict != original) or force_write_anyway:
                database_file.seek(0)
                database_file.truncate()
                database_file.write(jsondumps(database_dict, indent=4))
                database_file.flush()

def get_or_set(d: dict, key: str, default):
    if key not in d: d[key] = default
    return d[key]