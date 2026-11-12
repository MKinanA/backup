from argparse import ArgumentParser, _SubParsersAction, Namespace
from .utils.database import database_read

def register_subparser(subparsers: _SubParsersAction[ArgumentParser]):
    parser = subparsers.add_parser('list', help='List created backup profiles.')
    parser.set_defaults(func=execute)

def execute(args: Namespace):
    profiles: list = database_read().get('profiles', [])
    for profile in profiles: print(profile['name'])