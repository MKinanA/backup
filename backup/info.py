from argparse import ArgumentParser, _SubParsersAction, Namespace
from .utils.database import database_read, get_or_set
from .utils.expected_exception import expected_exception as expected

def register_subparser(subparsers: _SubParsersAction[ArgumentParser]):
    parser = subparsers.add_parser('info', help='Check the information (fields) of a backup profile.')
    parser.add_argument('name', type=str, help='Name of the backup profile.')
    parser.set_defaults(func=execute)

def execute(args: Namespace):
    profile_name = args.name
    profiles = get_or_set(database_read(), 'profiles', [])
    if not profile_name in (profile['name'] for profile in profiles): raise expected(KeyError(f'Profile "{profile_name}" doesn\'t exist.'))
    profile: dict = profiles[next((index for index in range(len(profiles)) if profiles[index]['name'] == profile_name))]
    longest_field_name = max(len(field_name) for field_name in profile.keys())
    for field, value in profile.items(): print(f'{field}{' ' * (longest_field_name - len(str(field)))}: {'"' if type(value) == str else ''}{value}{'"' if type(value) == str else ''}')