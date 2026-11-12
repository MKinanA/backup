from argparse import ArgumentParser, _SubParsersAction, Namespace
from pathlib import Path
from crontab import CronTab, CronSlices
from .utils.database import database_read, get_or_set
from .utils.expected_exception import expected_exception as expected

UNSCHEDULING_KEYWORDS = ('unschedule', 'delete', 'remove', 'none', 'null', 'never', 'inactive', 'deactivate', 'disable')

def register_subparser(subparsers: _SubParsersAction[ArgumentParser]):
    parser = subparsers.add_parser('schedule', help='Schedule a backup profile to run automatically.')
    parser.add_argument('name', type=str, help='Name of the backup profile.')
    parser.add_argument('-s', '--set', metavar='<cron_expression>', type=validate_schedule_expression, help=f'Either a cron expression for the scheduling, or {'/'.join(UNSCHEDULING_KEYWORDS)} to unschedule the profile.')
    parser.set_defaults(func=execute)

def execute(args: Namespace):
    # return # TODO: Unfinished
    profile_name = args.name
    profiles = get_or_set(database_read(), 'profiles', [])
    if not profile_name in (profile['name'] for profile in profiles): raise expected(KeyError(f'Profile "{profile_name}" doesn\'t exist.'))

def validate_schedule_expression(expression: str) -> str | None:
    if CronSlices.is_valid(expression): return expression
    elif expression.lower() in UNSCHEDULING_KEYWORDS: return None
    else: raise expected(ValueError('Invalid cron schedule expression.'))