# ======================================================================
# Class Application:
# - For invoking the application from the command line.
# ======================================================================
import argparse


def run():
    args = _parse_args()
    if args.action == 'r':
        print('Application.run():', 'args.action == r')
        # from ..app.services import ratings
        # cfc_mdb_update.update(
        #     args.cmu_members,
        #     args.cmu_cfcmdb,
        #     args.cmu_cfcmdb_pw
        # )
    else:
        print(f'Unknown action: "{args.action}"')

def _parse_args():
    ap = argparse.ArgumentParser(description='CFC-Server: command line tasks')
    ap.add_argument('-a', '--action', dest='action', required=True,
                    choices=['j', 'r'],
                    help='Action: j=job; r=ratings; ')
    ap.add_argument('-j', '--job', dest='job',
                    help='Name of the directory containing the job')
    ap.add_argument('--dev', dest='is_dev', action='store_true',
                    help='Use development\'s configuration values')
    return ap.parse_args()
