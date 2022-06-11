# ======================================================================
# CLI - Command Line Interface
# ======================================================================
import sys, argparse
import logging
log = logging.getLogger('app')
log.setLevel(logging.INFO)


def run():
    args = _parse_args()
    if args.job:
        from cfcserver.services import jobs as s_jobs
        error = s_jobs.run_job(args.job)
        if error:
            sys.exit(error)
    elif args.action == 'cfcdb':
        from cfcserver.services import cfcdb as s_cfcdb
        s_cfcdb.create(args.job)
    else:
        sys.exit(f'ERROR: Unknown action: "{args.action}"')


def _parse_args():
    ap = argparse.ArgumentParser(description='CFC-Server: command line tasks')
    ap.add_argument('--cli', dest='action', required=False,
        choices=['r', 'cfcdb'],
        help='Action: rc=ratings-create; ')
    ap.add_argument('-j', '--job', dest='job', required=False,
        help='Name of the directory containing the job')
    ap.add_argument('--local', dest='is_local', action='store_true',
        help='Use local directories')
    ap.add_argument('--dev', dest='is_dev', action='store_true',
        help='Use development\'s configuration values')
    return ap.parse_args()


# ======================================================================
# Dev Notes:
# - Cannot import cfcserver outside of run() since app is not fully
#   initialized yet; it causes undefined or circular import errors.
