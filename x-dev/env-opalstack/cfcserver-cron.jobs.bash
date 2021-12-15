#!/bin/bash
#-----------------------------------------------------------------------
# CFC Server Cron Job:
#-----------------------------------------------------------------------
set -euo pipefail

readonly APP_ROOT="/home/don/apps/cfc_server"
readonly APP_LOCAL="${APP_ROOT}/app_local"
export CFCSERVER_CONFIG_FILE="${APP_LOCAL}/config/app.config"
export TZ="America/Toronto"
readonly CRON_LOG_FILE="${APP_LOCAL}/logs/cron-log.jobs.$(date +"%Y-%m-%d").txt"

# TODO: Remove after switch to V1 APIs
export APP_CONFIG_DIR="${APP_LOCAL}/config"
export APP_DATA_DIR="${APP_LOCAL}/data"
export APP_JOBS_DIR="${APP_LOCAL}/jobs"

function main {
  log $(basename $0) invoked

  local runnable=$(find ${APP_LOCAL}/jobs -mindepth 2 -maxdepth 2 -name job.runnable)
  for jobrunnable in ${runnable}; do
    log Found a runnable job in $(basename ${jobrunnable})

    local jobdir=$(dirname ${jobrunnable})
    local jobdir_basename=$(basename ${jobdir})

    mv "${jobrunnable}" "${jobdir}/job.running"
    source "${APP_ROOT}/deployed/venv/bin/activate"
    python3.9 "${APP_ROOT}/deployed/main.py" --job "${jobdir_basename}"
    mv "${jobdir}/job.running" "${jobdir}/job.ended"
  done
}

function log {
  echo $(date +"%Y-%m-%d-%T"): "$@"
}

main >>$CRON_LOG_FILE 2>&1
