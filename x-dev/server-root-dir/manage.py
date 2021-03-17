#!/usr/bin/env python3
# ======================================================================
# manage.py
#   - Deploy a release of code from Gitlab to Opalstack & activate it.
#   - Install:  Copy to ~/apps/myapp; update the vars at the top;
#     then it invoke as "./manage.py <action>"
#       - "start"
#       - "stop"
#       - "kill"
#       - "deploy"
#   - This script may run in a Python version earlier than what is
#     required by the application.  The Python version required by
#     may need to be installed if it is not provided by Opalstack.
#     For example, Python 3.9 was installed in /home/don/opt
# ======================================================================
# Config:
git_repos = 'https://gitlab.com/parakin/cfc-server.git'
app_dir = '/home/don/apps/cfc_server'
python_bin = '/home/don/opt/bin/python3.9'
deploy_dir_prefix = 'deploy-'
# Derived
pid_file = app_dir + '/tmp/cfc_server.pid'
uwsgi_ini_file = app_dir + '/uwsgi.ini'
uwsgi_bin = app_dir + '/deployed/venv/bin/uwsgi'

# ======================================================================
import sys, os, logging, subprocess, shutil
if sys.version_info < (3,4):    # need pathlib
    raise Exception('FATAL: This script requires Python 3.4 or later.')
from pathlib import Path

logging.basicConfig(level=logging.INFO, datefmt='%H:%M:%S', format='%(asctime)s: %(message)s')
log = logging.getLogger()


def main():
    actions = {'start': action_start, 'stop': action_stop, 'kill': action_kill, 'deploy': action_deploy}
    if len(sys.argv) < 2:
        print('Action not specified. Actions are start|stop|kill|deploy')
    elif sys.argv[1] in actions:
        actions[sys.argv[1]]()
    else:
        print('Invalid action "%s"'.format(sys.argv[1]))


# ---------------- start | stop | kill
def action_start():
    uwsgi_pid = get_uwsgi_pid()
    if uwsgi_pid in get_users_pids():
        log.info('Already running (pid=%s)', uwsgi_pid)
    else:
        subprocess.run([uwsgi_bin, '--ini', uwsgi_ini_file], check=True)
        uwsgi_pid = get_uwsgi_pid()
        log.info('Started uWSGI (pid=%s)', uwsgi_pid)


def action_stop():
    uwsgi_pid = get_uwsgi_pid()
    if uwsgi_pid is None:
        log.info('Not running (pid file not found)')
    elif uwsgi_pid not in get_users_pids():
        log.info('Not running (pid=%s not found)', uwsgi_pid)
    else:
        subprocess.run([uwsgi_bin, '--stop', pid_file], check=True)
        subprocess.run(['rm', pid_file], check=True)
        log.info('uWSGI stopped (pid was %s)', uwsgi_pid)


def action_kill():
    uwsgi_pid = get_uwsgi_pid()
    if uwsgi_pid is None:
        log.info('Not running (pid file not found)')
    elif uwsgi_pid not in get_users_pids():
        log.info('Not running (pid=%s not found)', uwsgi_pid)
    else:
        subprocess.run(['kill', '-9', uwsgi_pid], check=False)
        log.info('uWSGI killed (pid was %s)', uwsgi_pid)


def get_uwsgi_pid():
    if not Path(pid_file).exists():
        return None
    with open(pid_file, 'rb') as f:
        pid = f.read().strip()
    return pid

def get_users_pids():
    out = dict(stdout=subprocess.PIPE)
    user = subprocess.run('whoami', **out).stdout.strip()
    cmd = ['ps', '-u', user, '-opid=']
    pids = subprocess.run(cmd, **out).stdout
    return pids.split()


# ---------------- deploy
def action_deploy():
    application_dir = Path(app_dir).resolve()
    deploy_dir = get_next_deploy_dir(application_dir)
    git_clone(deploy_dir)
    venv_dir = venv_create(deploy_dir)
    pip_install_requirements(deploy_dir, venv_dir)
    pip_install_uwsgi(venv_dir)
    set_current_deploy(deploy_dir)
    restart_uwsgi(application_dir)


def get_next_deploy_dir(application_dir):
    log.info('---- ---- ---- ---- deploy')
    log.info('Git repo: %s', git_repos)
    deploy_n = 1
    deploy_list = sorted(application_dir.glob(deploy_dir_prefix + '*'), reverse=True)
    for d in deploy_list:
        num = d.name[len(deploy_dir_prefix):]
        if len(num) > 0 and num.isdigit():
            deploy_n = 1 + int(num)
            break
    dirname = '{}{:04d}'.format(deploy_dir_prefix, deploy_n)
    log.info('Next dir: %s', dirname)
    return application_dir / dirname


def git_clone(deploy_dir):
    log.info('---- ---- git clone')
    cmd = ['git', 'clone', git_repos, str(deploy_dir)]
    subprocess.run(cmd, check=True)
    if deploy_dir.exists():
        # -- Delete unneeded directories (save some space)
        dir_list = ['.git', '.idea']
        for dir in dir_list:
            p = deploy_dir / dir
            if p.exists():
                shutil.rmtree(str(p), ignore_errors=True)


def venv_create(deploy_dir):
    log.info('---- ---- venv create')
    venv_dir = deploy_dir / 'venv'
    cmd = [python_bin, '-m', 'venv', str(venv_dir), '--prompt', deploy_dir.name, '--upgrade-deps']
    cp = subprocess.run(cmd)
    cp.check_returncode()
    return venv_dir


def pip_install_requirements(deploy_dir, venv_dir):
    log.info('---- ---- pip install -r requirements.frozen.txt')
    os_env = os.environ.copy()
    os_env['VIRTUAL_ENV'] = str(venv_dir)
    os_env['PATH'] = '{}/bin:{}'.format(venv_dir, os_env['PATH'])
    pip_reqs = deploy_dir / 'x-dev' / 'python' / 'requirements.frozen.txt'
    cmd = ['pip', 'install', '-r', str(pip_reqs)]
    subprocess.run(cmd, env=os_env, check=True)


def pip_install_uwsgi(venv_dir):
    log.info('---- ---- pip install uwsgi')
    os_env = os.environ.copy()
    os_env['VIRTUAL_ENV'] = str(venv_dir)
    os_env['PATH'] = '{}/bin:{}'.format(venv_dir, os_env['PATH'])
    cmd = ['pip', 'install', 'uwsgi']
    subprocess.run(cmd, env=os_env, check=True)


def set_current_deploy(deploy_dir):
    log.info('---- ---- set ./deployed -> ./' + deploy_dir.name)
    cmd = ['ln', '-fns', deploy_dir.name, 'deployed']
    subprocess.run(cmd, check=True)


def restart_uwsgi(application_dir):
    log.info('---- ---- uwsgi: restart')
    cmd = ['touch', str(application_dir / 'touch-to-reload.txt')]
    subprocess.run(cmd, check=True)


main()
