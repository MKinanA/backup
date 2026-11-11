from argparse import ArgumentParser, _SubParsersAction, Namespace
from pathlib import Path
from .delete import execute as delete
from .create import execute as create
from .utils.database import database_read, get_or_set
from .utils.expected_exception import expected_exception as expected

def register_subparser(subparsers: _SubParsersAction[ArgumentParser]):
    parser = subparsers.add_parser('modify', help='Modify an existing backup schema.')
    parser.add_argument('name', type=str, help='Name of the existing backup schema to modify.')
    parser.add_argument('--source-path', '--source', type=Path, help='New location of the backup source (what you want to back up), can be either a file or a directory (folder).')
    parser.add_argument('--backup-path', '--backup', type=Path, help='New location of the backup destination (where you want the backups stored), must be a directory (duhh).')
    parser.set_defaults(func=execute)

def execute(args: Namespace):
    schema_name = args.name
    schemas = get_or_set(database_read(), 'schemas', [])
    if not schema_name in (schema['name'] for schema in schemas): raise expected(KeyError(f'Schema "{schema_name}" doesn\'t exist.'))
    schema: dict = schemas[next((index for index in range(len(schemas)) if schemas[index]['name'] == schema_name))]
    source_path = Path(schema['source_path']).resolve()
    backup_path = Path(schema['backup_path']).resolve()

    modifications = []
    if (new_source_path := args.source_path) is not None and (new_source_path.resolve() != (source_path)): modifications.append('source_path')
    elif new_source_path is None: args.source_path = source_path
    if (new_backup_path := args.backup_path) is not None and (new_backup_path.resolve() != (backup_path)): modifications.append('backup_path')
    elif new_backup_path is None: args.backup_path = backup_path

    if len(modifications) > 0:
        print('> ', end='')
        delete(args)
        print('> ', end='')
        create(args)
        print(f'Modified {f'{',' if len(modifications) > 2 else ''} '.join(f'{'and ' if (index >= (len(modifications) - 1)) and (len(modifications) > 1) else ''}`{field}`' for index, field in enumerate(modifications))} of backup schema "{schema_name}".')
    else: print('Nothing changed.')