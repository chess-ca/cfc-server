#!/usr/bin/env bash
# ======================================================================
# deploy.bash
# ======================================================================
readonly app_dir="/home/don/apps/cfc_server"
readonly python_version="3.9"
readonly python_bin="/home/don/opt/bin/python3.9"
readonly git_repos="https://gitlab.com/parakin/cfc-server.git"


main() {
  deploy_dirname=$( get_next_deploy_dirname )
  git_clone "${deploy_dirname}"
  venv_create "${deploy_dirname}"
  pip_install "${deploy_dirname}"
  pip_install_uwsgi "${deploy_dirname}"
  set_current_deploy "${deploy_dirname}"
  restart_uwsgi
}

get_next_deploy_dirname() {
  # Note: Must remove leading zeros else will be octal, not base-10
  last_n=$( find "${app_dir}" -maxdepth 1 -regex '.*/deploy-[0-9]+$' \
    | sed -n -e 's/.*\/deploy-0*//p' \
    | awk 'BEGIN {max=0} $0 > max {max=$0} END {print max}' )
  next_n=$(( last_n + 1 ))
  echo $(printf "deploy-%04d" $next_n)
}

git_clone() {
  deploy_dir="${app_dir}/$1"
  log "---- ---- Git: clone"
  log "Cloning git repos: ${git_repos}"
  git clone "${git_repos}" "${deploy_dir}"
  if [[ -d "${deploy_dir}" ]]; then
    # -- To save space, delete unneeded directories
    rm -fr -- "${deploy_dir}/.git"
    rm -fr -- "${deploy_dir}/.idea"
  fi
  log "Done!"
}

venv_create() {
  deploy_dirname="$1"
  deploy_dir="${app_dir}/$1"
  log "---- ---- venv create"
  "${python_bin}" -m venv "${deploy_dir}/venv" \
    --prompt "${deploy_dirname}" \
    --upgrade-deps
  log "Done!"
}

pip_install() {
  deploy_dir="${app_dir}/$1"
  log "---- ---- pip install"
  pip_reqs="${deploy_dir}/x-dev/python/requirements.frozen.txt"
  source "${deploy_dir}/venv/bin/activate"
  pip3 install -r "${pip_reqs}"
  deactivate
  log "Done!"
}

pip_install_uwsgi() {
  # Must install uwsgi separately for Opalstack (it won't install on Windows)
  deploy_dir="${app_dir}/$1"
  log "---- ---- pip install uwsgi (needed by Opalstack)"
  source "${deploy_dir}/venv/bin/activate"
  pip3 install uwsgi
  deactivate
  log "Done!"
}

set_current_deploy() {
  deploy_dir="${app_dir}/$1"
  log "---- ---- set ./deployed -> ./$1"
  ln -fns "$deploy_dir" "deployed"
  ls -ld "deployed"
  log "Done!"
}

restart_uwsgi() {
  deploy_dir="${app_dir}/$1"
  log "---- ---- uwsgi: restart"
  touch "${deploy_dir}/touch-to-reload.txt"
  log "Done!"
}

log() {
  echo $(date +"%T") "$@"
}

main "${@}"
