from argparse import ArgumentParser, _SubParsersAction, Namespace
from pathlib import Path
from .utils.database import database_write, get_or_set
from .utils.expected_exception import expected_exception as expected

def register_subparser(subparsers: _SubParsersAction[ArgumentParser]):
    parser = subparsers.add_parser('create', help='Create a new backup profile.')
    parser.add_argument('name', type=str, help='Name of the backup profile.')
    parser.add_argument('source_path', type=Path, help='Location of the backup source (what you want to back up), can be either a file or a directory (folder).')
    parser.add_argument('backup_path', type=Path, help='Location of the backup destination (where you want the backups stored), must be a directory (duhh).')
    parser.set_defaults(func=execute)

def execute(args: Namespace):
    profile_name = args.name
    with database_write() as db:
        profiles: list = get_or_set(db, 'profiles', [])
        if profile_name in (profile['name'] for profile in profiles): raise expected(ValueError(f'Backup profile named "{profile_name}" already exists.'))
        else: profiles.append({
            'name': profile_name,
            'source_path': str(args.source_path.resolve()),
            'backup_path': str(args.backup_path.resolve()),
        })
    print(f'Created new backup profile "{profile_name}".')