#!/bin/bash
#-----------------------------------------------------------------------
# CFC Server Cron Job:
#-----------------------------------------------------------------------
APP_ROOT=/home/don/apps/cfc_server
APP_LOCAL=$APP_ROOT/app_local

export TZ=America/Toronto
export CFCSERVER_CONFIG_FILE=$APP_LOCAL/config/app.config
LOG_FILE=$APP_LOCAL/logs/cron-log.jobs.$(date +"%Y-%m-%d").txt

# TODO: Remove after switch to V1 APIs
export APP_CONFIG_DIR="$APP_LOCAL/config"
export APP_DATA_DIR="$APP_LOCAL/data"
export APP_JOBS_DIR="$APP_LOCAL/jobs"


function main {
  echo $(date +"%Y-%m-%d-%T"): $(basename $0) invoked

  source "$APP_ROOT/deployed/venv/bin/activate"

  python3.9 "$APP_ROOT/deployed/main.py" --cli jobs
}

main >>$LOG_FILE 2>&1
