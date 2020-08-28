#!/usr/bin/env python3.8

from pathlib import Path
import subprocess, shutil, configparser

_py_version = '3.8'
_git_repos = 'https://gitlab.com/parakin/cfc-server.git'

_prefix = 'deploy-'
_project_dir = Path(__file__).parent
_deploy_config = Path(_project_dir, 'current-deploy.conf')

_config_file = Path(_project_dir, 'wsgi_start.config')
_current_deploy_file = Path(_project_dir, 'wsgi-start.current-deploy.txt')


def main():
    deploy_dir = get_next_deploy_dir()
    git_clone(deploy_dir)
    pip_install(deploy_dir)
    set_current_deploy_dir(deploy_dir)
    # restart_apache2()


def get_next_deploy_dir():
    deploy_n = 1
    deploy_list = sorted(_project_dir.glob(_prefix + '*'), reverse=True)
    for d in deploy_list:
        num = d.name[len(_prefix):]
        if len(num) > 0 and num.isdigit():
            deploy_n = 1 + int(num)
            break
    return '{}{:04d}'.format(_prefix, deploy_n)


def git_clone(deploy_dir):
    print('---- ---- ---- ---- Git: clone')
    d_dir = Path(_project_dir, deploy_dir)
    cmd = ['git', 'clone', _git_repos, str(d_dir)]
    cp = subprocess.run(cmd)
    cp.check_returncode()
    if d_dir.exists():
        git_dir = Path(d_dir, '.git')
        if git_dir.exists():    # delete unused .git/** to save space
            shutil.rmtree(str(git_dir), ignore_errors=True)


def pip_install(deploy_dir):
    print('---- ---- ---- ---- pip install')
    pip_reqs = str(Path(_project_dir, deploy_dir, 'x-dev', 'python', 'requirements.frozen.txt'))
    pylib_dir = str(Path(_project_dir, deploy_dir, 'lib', f'python{_py_version}'))
    cmd = [f'pip{_py_version}', 'install', '-r', pip_reqs, '-t', pylib_dir]
    cp = subprocess.run(cmd)
    cp.check_returncode()


def set_current_deploy_dir(deploy_dir):
    with open(str(_current_deploy_file), 'w') as f:
        f.write(deploy_dir)


def restart_apache2():
    print('---- ---- ---- ---- Apache: restart')
    cmd = [str(Path(_project_dir, 'apache2', 'bin', 'restart'))]
    cp = subprocess.run(cmd)
    cp.check_returncode()


main()
