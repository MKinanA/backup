from contextlib import contextmanager
from pathlib import Path
from json import loads as jsonloads, dumps as jsondumps
from copy import deepcopy
from .open_file_with_lock import open_file_with_lock

DATABASE_PATH = (Path(__file__).parent.parent / 'database.json').resolve()

def database_read() -> dict:
    with open(DATABASE_PATH, 'r') as database_file: return jsonloads(database_file.read())

@contextmanager
def database_write():
    with open_file_with_lock(DATABASE_PATH) as database_file:
        database_dict = jsonloads(database_file.read())
        original = deepcopy(database_dict)
        try: yield database_dict
        except: raise
        else:
            if database_dict != original:
                database_file.seek(0)
                database_file.truncate()
                database_file.write(jsondumps(database_dict, indent=4))
                database_file.flush()