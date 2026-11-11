from argparse import ArgumentParser, _SubParsersAction, Namespace
from pathlib import Path
from hashlib import file_digest as hash
from datetime import datetime
from tarfile import open as opentar
from .validate import validate_schema
from .utils.database import database_read, get_or_set
from .utils.expected_exception import expected_exception as expected

BACKUP_ARCHIVE_FILE_EXTENSION = '.tar.gz'
BACKUP_ARCHIVE_HASH_ALGORITHM = 'sha256'
BACKUP_ARCHIVE_TIMESTAMP_FORMAT = '%Y-%m-%d-%H-%M-%S'

def register_subparser(subparsers: _SubParsersAction[ArgumentParser]):
    parser = subparsers.add_parser('run', help='Run a backup schema, creating an archive of the source file/directory and storing it in the backup directory.')
    parser.add_argument('name', type=str, help='Name of the backup schema.')
    parser.set_defaults(func=execute)

def execute(args: Namespace):
    schema_name = args.name
    schemas = get_or_set(database_read(), 'schemas', [])
    if not schema_name in (schema['name'] for schema in schemas): raise expected(KeyError(f'Schema "{schema_name}" doesn\'t exist.'))
    schema: dict = schemas[next((index for index in range(len(schemas)) if schemas[index]['name'] == schema_name))]
    validate_schema(schema)

    with opentar(backup_tar_path := ((backup_path := Path(schema['backup_path'])) / f'{schema_name} {datetime.now().strftime(BACKUP_ARCHIVE_TIMESTAMP_FORMAT)}{BACKUP_ARCHIVE_FILE_EXTENSION}'), 'w:gz') as backup_tar:
        if (source_path := Path(schema['source_path'])).is_dir():
            print('`source_path` is a directory, iterating...')
            for path in source_path.iterdir():
                print(f'> {path.name}')
                backup_tar.add(path, arcname=path.name)
        else:
            print('`source_path` is not a directory, copying into backup archive...')
            backup_tar.add(source_path, arcname=source_path.name)
    with open(backup_tar_path, 'rb') as backup_tar: backup_tar_path.rename(backup_tar_path := (backup_tar_path.parent / f'{backup_tar_path.name[:-len(BACKUP_ARCHIVE_FILE_EXTENSION)]} {(checksum := hash(backup_tar, BACKUP_ARCHIVE_HASH_ALGORITHM).hexdigest())}{BACKUP_ARCHIVE_FILE_EXTENSION}'))
    print(f'Done, backup archive stored in `{backup_path}` as `{backup_tar_path.name}`.\nChecksum is "{checksum}" ({BACKUP_ARCHIVE_HASH_ALGORITHM}).')