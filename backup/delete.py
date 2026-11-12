from argparse import ArgumentParser, _SubParsersAction, Namespace
from .utils.database import database_write, get_or_set
from .utils.expected_exception import expected_exception as expected

def register_subparser(subparsers: _SubParsersAction[ArgumentParser]):
    parser = subparsers.add_parser('delete', help='Delete a backup profile.')
    parser.add_argument('name', type=str, help='Name of the backup profile.')
    parser.set_defaults(func=execute)

def execute(args: Namespace):
    profile_name = args.name
    with database_write() as db:
        if 'profiles' not in db: return
        profiles = get_or_set(db, 'profiles', [])
        if not profile_name in (profile['name'] for profile in profiles): raise expected(KeyError(f'Profile "{profile_name}" doesn\'t exist.'))
        del profiles[next((index for index in range(len(profiles)) if profiles[index]['name'] == profile_name))]
    print(f'Deleted backup profile "{profile_name}".')