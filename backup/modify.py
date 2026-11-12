from argparse import ArgumentParser, _SubParsersAction, Namespace
from pathlib import Path
from .delete import execute as delete
from .create import execute as create
from .utils.database import database_read, get_or_set
from .utils.expected_exception import expected_exception as expected

def register_subparser(subparsers: _SubParsersAction[ArgumentParser]):
    parser = subparsers.add_parser('modify', help='Modify an existing backup profile.')
    parser.add_argument('name', type=str, help='Name of the existing backup profile to modify.')
    parser.add_argument('--source-path', '--source', type=Path, help='New location of the backup source (what you want to back up), can be either a file or a directory (folder).')
    parser.add_argument('--backup-path', '--backup', type=Path, help='New location of the backup destination (where you want the backups stored), must be a directory (duhh).')
    parser.set_defaults(func=execute)

def execute(args: Namespace):
    profile_name = args.name
    profiles = get_or_set(database_read(), 'profiles', [])
    if not profile_name in (profile['name'] for profile in profiles): raise expected(KeyError(f'Profile "{profile_name}" doesn\'t exist.'))
    profile: dict = profiles[next((index for index in range(len(profiles)) if profiles[index]['name'] == profile_name))]
    source_path = Path(profile['source_path']).resolve()
    backup_path = Path(profile['backup_path']).resolve()

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
        print(f'Modified {f'{',' if len(modifications) > 2 else ''} '.join(f'{'and ' if (index >= (len(modifications) - 1)) and (len(modifications) > 1) else ''}`{field}`' for index, field in enumerate(modifications))} of backup profile "{profile_name}".')
    else: print('Nothing changed.')