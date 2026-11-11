from argparse import ArgumentParser, _SubParsersAction, Namespace
from pathlib import Path
from hashlib import file_digest as hash
from datetime import datetime
from .validate import validate_schema
from .run import BACKUP_ARCHIVE_HASH_ALGORITHM, BACKUP_ARCHIVE_FILE_EXTENSION, BACKUP_ARCHIVE_TIMESTAMP_FORMAT
from .utils.database import database_read, get_or_set

def register_subparser(subparsers: _SubParsersAction[ArgumentParser]):
    parser = subparsers.add_parser('check', help='Check the backup archives stored in the backup path of a backup schema using their checksums for integrity.')
    parser.add_argument('name', type=str, help='Name of the backup schema.')
    parser.set_defaults(func=execute)

def execute(args: Namespace):
    schema_name = args.name
    schemas = get_or_set(database_read(), 'schemas', [])
    if not schema_name in (schema['name'] for schema in schemas): raise KeyError(f'(expected) Schema "{schema_name}" doesn\'t exist.')
    schema: dict = schemas[next((index for index in range(len(schemas)) if schemas[index]['name'] == schema_name))]
    validate_schema(schema, only=('backup_path',))

    files = 0
    checked_files = 0
    checksum_mismatches = 0
    for backup_tar_path in Path(schema['backup_path']).iterdir():
        if backup_tar_path.is_file() and (files := files + 1) and ((backup_name_parsed := parse_backup_name(backup_name := backup_tar_path.name)) is not None) and (backup_name_parsed[0] == schema_name) and (checked_files := checked_files + 1):
            with open(backup_tar_path, 'rb') as backup_tar: print(f'> {backup_name}: {'OK' if hash(backup_tar, BACKUP_ARCHIVE_HASH_ALGORITHM).hexdigest() == backup_name_parsed[2] else ((checksum_mismatches := checksum_mismatches + 1) and 'WARNING: CHECKSUM MISMATCH!')}')
    print(f'Total: {checksum_mismatches} checksum mismatch{'es' if checksum_mismatches > 1 else ''} out of {checked_files} recognized backup archive file{'s' if checked_files > 1 else ''} (out of all {files} file{'s' if files > 1 else ''} inside the backup directory).\n{'Check your backup archive files.' if checksum_mismatches > 0 else ('Do you store other files in the directory?' if files > checked_files else 'Good.')}')
    if checksum_mismatches > 0: return 1

def parse_backup_name(name: str, raise_on_invalid: bool = False) -> tuple[str, datetime, str] | None:
    try:
        if (not name.endswith(BACKUP_ARCHIVE_FILE_EXTENSION)) or (len(parts := name[:-len(BACKUP_ARCHIVE_FILE_EXTENSION)].split(' ')) < 3) or (not (timestamp := datetime.strptime(parts[-2], BACKUP_ARCHIVE_TIMESTAMP_FORMAT))) or (len(parts[-1]) != 64) or any((char.lower() not in (*(str(x) for x in range(0, 10)), *'abcdef')) for char in parts[-1]):
            if raise_on_invalid: raise ValueError
            else: return None
    except ValueError: raise ValueError(f'(expected) The backup archive filename doesn\'t appear to be in the expected format (containing the backup schema name, a valid timestamp in a specific format, a 64-character SHA-256 hash checksum, and the `{BACKUP_ARCHIVE_FILE_EXTENSION}` extension).')
    return (' '.join(parts[:-2]), timestamp, parts[-1])