from os import fstat, replace
from contextlib import contextmanager
from pathlib import Path
from json import loads as jsonloads, dumps as jsondumps, JSONDecodeError
from copy import deepcopy
from .open_file_with_lock import open_file_with_lock

DATABASE_PATH = (Path(__file__).parent.parent / 'database.json').resolve()
TEMP_DATABASE_PATH = Path(str(DATABASE_PATH) + '.tmp')
MAX_READ_ATTEMPTS = 2
MAX_WRITE_ATTEMPTS = 10

def database_read() -> dict:
    attempts = 0
    exc = None
    while attempts < MAX_READ_ATTEMPTS:
        attempts += 1
        database_raw = None
        try:
            with open_file_with_lock(DATABASE_PATH, shared_readonly=True) as database_file: return jsonloads(database_raw := database_file.read())
        except (JSONDecodeError, FileNotFoundError) as e:
            exc = e
            if not database_raw:
                with database_write(): pass
            else: raise
    raise RuntimeError('Failed to parse database.') from exc

@contextmanager
def database_write():
    force_write_anyway = False
    attempts = 0
    while attempts < MAX_WRITE_ATTEMPTS:
        attempts += 1
        with open_file_with_lock(DATABASE_PATH) as database_file:
            try:
                if ((database_file_stat := fstat(database_file.fileno())).st_dev, database_file_stat.st_ino) != ((database_path_stat := DATABASE_PATH.stat()).st_dev, database_path_stat.st_ino): continue
            except FileNotFoundError: continue
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
                    with open_file_with_lock(TEMP_DATABASE_PATH) as temp_database_file:
                        temp_database_file.seek(0)
                        temp_database_file.truncate()
                        temp_database_file.write(jsondumps(database_dict, indent=4))
                    replace(TEMP_DATABASE_PATH, DATABASE_PATH)
        return
    raise RuntimeError('Failed to access database.')

def get_or_set(d: dict, key: str, default):
    if key not in d: d[key] = default
    return d[key]