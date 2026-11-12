from argparse import ArgumentParser, _SubParsersAction, Namespace
from pathlib import Path
from .utils.database import database_read, get_or_set
from .utils.expected_exception import expected_exception as expected

def register_subparser(subparsers: _SubParsersAction[ArgumentParser]):
    parser = subparsers.add_parser('validate', help='Validate a backup profile, such as checking the provided paths.')
    parser.add_argument('name', type=str, help='Name of the backup profile.')
    parser.set_defaults(func=execute)

def execute(args: Namespace):
    profile_name = args.name
    profiles = get_or_set(database_read(), 'profiles', [])
    if not profile_name in (profile['name'] for profile in profiles): raise expected(KeyError(f'Profile "{profile_name}" doesn\'t exist.'))
    profile: dict = profiles[next((index for index in range(len(profiles)) if profiles[index]['name'] == profile_name))]
    validate_profile(profile)
    print(f'Nothing wrong was detected in {profile_name}.')

def validate_profile(profile: dict, only: list[str] | tuple[str] | None = None):
    if ('source_path' in only if only is not None else True) and not Path(source_path := profile['source_path']).exists(): raise expected(FileNotFoundError(f'Source path `{source_path}` doesn\'t exist.'))
    if ('backup_path' in only if only is not None else True) and not ((backup_Path := Path(backup_path := profile['backup_path'])).exists() and backup_Path.is_dir()): raise expected(FileNotFoundError(f'Backup path `{backup_path}` doesn\'t exist or isn\'t a directory.'))