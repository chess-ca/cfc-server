#!/bin/bash
#-----------------------------------------------------------------------
# CFC Server Cron:  The Cleaner
#-----------------------------------------------------------------------
export TZ=America/Toronto
APP_LOCAL=/home/don/apps/cfc_server/app_local
LOGS_DIR=$APP_LOCAL/logs
CLEANER_LOG_FILE=$LOGS_DIR/cron-log.cleaner.$(date +"%Y-%m").txt
JOBS_DIR=$APP_LOCAL/jobs
JOBS_ARCHIVE_DIR=$APP_LOCAL/jobs/archive

function main {
  log $(basename ${0}) invoked
  cleaning_for_databases
  cleaning_for_jobs
  cleaning_for_the_cleaner
}

function cleaning_for_databases {
  pushd "${APP_LOCAL}/data/ratings"
  ls -r ratings.*.sqlite | tail -n +11 | xargs -r echo rm -fr
  ls -r ratings.*.sqlite | tail -n +11 | xargs -r rm -fr
  popd
  pushd "${APP_LOCAL}/data/cfcdb"
  ls -r cfcdb.*.sqlite | tail -n +11 | xargs -r echo rm -fr
  ls -r cfcdb.*.sqlite | tail -n +11 | xargs -r rm -fr
  popd
}

function cleaning_for_jobs {
  find $LOGS_DIR -maxdepth 1 -name 'cron-log.jobs.*.txt' -mtime +2 -execdir gzip {} \;
  find $LOGS_DIR -maxdepth 1 -name 'cron-log.jobs.*.txt.gz' -mtime +35 -delete

  old_jobs=$(find $JOBS_DIR -mindepth 2 -maxdepth 2 -name 'job.log' -mtime +35)
  for job_log in $old_jobs; do
    job_dir=$(dirname $job_log)
    log ... Moving $(basename $job_dir) to archive
    mv $job_dir $JOBS_ARCHIVE_DIR
    done

  old_archives=$(find $JOBS_ARCHIVE_DIR -mindepth 2 -maxdepth 2 -name 'job.log' -mtime +65)
  for job_log in $old_archives; do
    job_dir=$(dirname $job_log)
    log ... Deleting archived $(basename $job_dir)
    rm --recursive --force -- $job_dir
    done
}

function cleaning_for_the_cleaner {
  find $LOGS_DIR -maxdepth 1 -name 'cron-log.cleaner.*.txt' -mtime +7 -execdir gzip {} \;
  find $LOGS_DIR -maxdepth 1 -name 'cron-log.cleaner.*.txt.gz' -mtime +65 -delete
}

function log {
  echo $(date +"%Y-%m-%d-%T"): "$@"
}

main >>$CLEANER_LOG_FILE 2>&1
