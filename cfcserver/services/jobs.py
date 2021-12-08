
import pathlib, configparser, datetime, pytz, zipfile
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
        job = Job(job_dir, timezone=AppConfig.PYTZ_TIMEZONE)
        if job.error is not None:
            continue
        if job.status == 'uploaded' or job.status == 'retrying':
            if job.run_type == 'extract-from-cfc-mdb':
                run_extract_from_cfc_mdb(job)


def run_extract_from_cfc_mdb(job: Job):
    job.log(f'START: Job extract-from-cfc-mdb for {job.dirname}')
    job.ini_set('RUN', 'status', 'running')
    job.ini_save()

    job.log(f'START: Extracting data files from *.zip')
    with zipfile.ZipFile(str(job.zip_path), mode='r') as zip_f:
        for name in zip_f.namelist():
            if name == 'job.ini' or name == 'job.log':
                continue
            zip_f.extract(name, path=str(job.dir))
    job.log(f'DONE: Extracting data files from *.zip')

    job.log(f'START: Running ratings_created_db.create (old)')
    from cfcserver.services import ratings_create_db
    ratings_create_db.create(str(job.dirname))
    job.log(f'DONE: Running ratings_created_db.create (old)')

    job.log(f'START: Running cfcdb.create (new)')
    from cfcserver.services import cfcdb
    cfcdb.create(str(job.dirname))
    job.log(f'DONE: Running cfcdb.create (new)')

    job.ini_set('RUN', 'status', 'success')
    job.ini_set('RUN', 'run_after', '9999-12-31-00:00:00')
    job.ini_save()
    job.log(f'DONE: Job extract-from-cfc-mdb for {job.dirname}')


