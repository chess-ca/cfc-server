# ======================================================================
# CLI - Command Line Interface
# ======================================================================
import sys, argparse
import logging
log = logging.getLogger('app')
log.setLevel(logging.INFO)


def run():
    args = _parse_args()
    if args.action == 'r':
        from cfcserver.services import ratings_create_db
        ratings_create_db.create(args.job)
    elif args.action == 'rc':
        from cfcserver.services import ratings_create_db_v2
        ratings_create_db_v2.create(args.job)
    elif args.action == 'cfcdb':
        from cfcserver.services import cfcdb_create
        cfcdb_create.create(args.job)
    else:
        print(f'Unknown action: "{args.action}"')


def _parse_args():
    ap = argparse.ArgumentParser(description='CFC-Server: command line tasks')
    ap.add_argument('--cli', dest='action', required=True,
        choices=['r', 'rc', 'cfcdb'],
        help='Action: rc=ratings-create; ')
    ap.add_argument('-j', '--job', dest='job',
        help='Name of the directory containing the job')
    ap.add_argument('--local', dest='is_local', action='store_true',
        help='Use local directories')
    ap.add_argument('--dev', dest='is_dev', action='store_true',
        help='Use development\'s configuration values')
    return ap.parse_args()
