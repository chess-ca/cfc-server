# ======================================================================
# Class Application:
# - For invoking the application from the command line.
# ======================================================================
import argparse
import logging
log = logging.getLogger()
log.setLevel(logging.INFO)

def run():
    args = _parse_args()
    if args.action == 'r':
        from cfcserver.services import ratings_create_db
        ratings_create_db.create(args.job)
    else:
        print(f'Unknown action: "{args.action}"')

def _parse_args():
    ap = argparse.ArgumentParser(description='CFC-Server: command line tasks')
    ap.add_argument('-a', '--action', dest='action', required=True,
                    choices=['r'],
                    help='Action: r=ratings; ')
    ap.add_argument('-j', '--job', dest='job',
                    help='Name of the directory containing the job')
    ap.add_argument('--dev', dest='is_dev', action='store_true',
                    help='Use development\'s configuration values')
    return ap.parse_args()
