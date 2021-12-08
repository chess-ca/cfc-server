
import pathlib, configparser, datetime, pytz
from codeboy4py.py.jobs import Job
from cfcserver.models.appconfig import AppConfig


def jobs_list(details='', include_invalid=False) -> list:
    jobs_dir = pathlib.Path(AppConfig.JOBS_DIR)
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


def cli():
    """Run jobs (from CLI or cron)"""
    jobs_dir = pathlib.Path(AppConfig.JOBS_DIR).resolve()
    for job_dir in jobs_dir.iterdir():
        if not job_dir.is_dir():
            continue
        job = Job(job_dir, timezone='Canada/Eastern')
        if job.error is not None:
            continue
