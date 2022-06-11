
from pathlib import Path
from codeboy4py.py.jobs import Job
from cfcserver.models.appconfig import AppConfig


def jobs_list(details='', include_invalid=False) -> list:
    jobs_dir = Path(AppConfig.JOBS_DIR)
    job_list = []
    for job_dir in jobs_dir.iterdir():
        if not job_dir.is_dir():
            continue
        jobini = job_dir / 'job.ini'
        if not jobini.exists():
            continue    # its not a Job directory

        job = Job(job_dir, timezone=AppConfig.PYTZ_TIMEZONE)
        if job.error is None or include_invalid:
            job_list.append(job.get_info(details=details))
    return job_list


def run_job(job_dir_basename):
    """Run a job"""
    job_dir = Path(AppConfig.JOBS_DIR, job_dir_basename).resolve()
    job = Job(job_dir, timezone=AppConfig.PYTZ_TIMEZONE)
    if job.error:
        return f'ERROR: {job.error}'
    if job.status != 'uploaded' and job.status != 'retrying':
        return f'ERROR: Cannot run job since status is not "uploaded" or "retrying"\n\tin {job_dir}'

    if job.run_type == 'extract-from-cfc-mdb':
        run_extract_from_cfc_mdb(job)
    else:
        return f'ERROR: Unknown run_type "{job.run_type}"\n\tin {job_dir}'
    return None


def run_extract_from_cfc_mdb(job: Job):
    job.log(f'START: Job extract-from-cfc-mdb for {job.dirname}')
    job.ini_set('RUN', 'status', 'running')
    job.ini_save()

    job.log(f'START: Running cfcdb.create (new)')
    from cfcserver.services import cfcdb
    cfcdb.create(job)
    job.log(f'DONE: Running cfcdb.create (new)')

    job.ini_set('RUN', 'status', 'success')
    job.ini_set('RUN', 'run_after', '9999-12-31-00:00:00')
    job.ini_save()
    job.log(f'DONE: Job extract-from-cfc-mdb for {job.dirname}')
