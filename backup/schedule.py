from sys import executable
from shlex import quote
from argparse import ArgumentParser, _SubParsersAction, Namespace
from pathlib import Path
from typing import Literal
from crontab import CronTab, CronSlices, CronItem
from .utils.database import database_read, get_or_set
from .utils.expected_exception import expected_exception as expected

UNSCHEDULING_KEYWORDS = ('unschedule', 'delete', 'remove', 'none', 'null', 'never', 'inactive', 'deactivate', 'disable')
CRON_JOB_COMMENT_PREFIX = 'sbtfl'

cron = CronTab(user=True)

def register_subparser(subparsers: _SubParsersAction[ArgumentParser]):
    parser = subparsers.add_parser('schedule', help='Schedule a backup profile to run automatically.')
    parser.add_argument('name', type=str, help='Name of the backup profile.')
    parser.add_argument('-s', '--set', metavar='<cron_expression>', type=validate_schedule_expression, help=f'Either a cron expression for the scheduling, or {'/'.join(UNSCHEDULING_KEYWORDS)} to unschedule the profile.')
    parser.set_defaults(func=execute)

def execute(args: Namespace):
    profile_name = args.name
    profiles = get_or_set(database_read(), 'profiles', [])
    if not profile_name in (profile['name'] for profile in profiles): raise expected(KeyError(f'Profile "{profile_name}" doesn\'t exist.'))
    profile: dict = profiles[next((index for index in range(len(profiles)) if profiles[index]['name'] == profile_name))]

    job = profile_cron(profile_name)
    already_scheduled_before = job is not None
    if args.set is None:
        if job is None: print(f'Backup profile "{profile_name}" isn\'t scheduled yet.')
        else: print(f'Backup profile "{profile_name}" is scheduled with cron `{job.slices}`.')
    else:
        if args.set:
            if job is None: job = cron.new(
                command=f'(cd {quote(str(module_loc := Path(__file__).parent.parent.resolve()))} && {{ {(module_command := f'{quote(executable)} -m {quote(__name__.split('.')[0])}')} run {quote(profile_name)}; {module_command} check {quote(profile_name)}; }}; echo) >> {quote(str(module_loc / 'cron.log'))} 2>&1',
                comment=f'{CRON_JOB_COMMENT_PREFIX} {profile_name}',
            )
            if args.set: job.setall(args.set)
        elif job is not None: cron.remove(job)
        if job is not None: cron.write()
        print(f'Backup profile "{profile_name}" has been {'re' if already_scheduled_before else ''}scheduled, cron is set to `{job.slices}`.' if args.set and job is not None else f'Backup profile "{profile_name}" {'has been unscheduled (cron job removed)' if already_scheduled_before else 'isn\'t scheduled yet'}.')

def validate_schedule_expression(expression: str) -> str | Literal[False]:
    if CronSlices.is_valid(expression): return expression
    elif expression.lower() in UNSCHEDULING_KEYWORDS: return False
    else: raise expected(ValueError('Invalid cron schedule expression.'))

def profile_cron(profile_name) -> CronItem | None: return next((job for job in cron if job.comment == f'{CRON_JOB_COMMENT_PREFIX} {profile_name}'), None)