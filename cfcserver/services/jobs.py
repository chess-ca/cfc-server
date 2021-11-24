
import pathlib, configparser, datetime, pytz
from types import SimpleNamespace
from codeboy4py.py.zipfile import SimpleZipFile
from cfcserver.models.appconfig import AppConfig

_job_attrs = ['name', 'title', 'handler', 'status', 'comments', 'error',
    'dt_created', 'dt_uploaded', 'dt_last', 'uts_last', 'log']
_tz_eastern = pytz.timezone('Canada/Eastern')


def jobs_list() -> list:
    jobs_dir = pathlib.Path(AppConfig.JOBS_DIR)
    job_list = []
    for job_dir in jobs_dir.iterdir():
        if not job_dir.is_dir(): continue
        job = job_info(job_dir.name, details=0)
        job_list.append(job)
    return job_list


def job_info(job_name: str, details=0):
    job = SimpleNamespace(**{ k: None for k in _job_attrs })
    job.name = job_name
    job_dir = pathlib.Path(AppConfig.JOBS_DIR, job_name)
    if not job_dir.exists():
        job.error = 'Job directory not found'
        return job

    # ---- From job.log
    job_log = job_dir / 'job.log'
    job.uts_last = job_log.stat().st_mtime if job_log.exists() \
        else job_dir.stat().st_mtime
    dt = datetime.datetime.fromtimestamp(job.uts_last, tz=_tz_eastern)
    job.dt_last = dt.strftime('%Y-%m-%d-%H:%M')

    # ---- From job.ini inside the .zip file:
    job_zip_fnames = [n for n in job_dir.glob('*.zip')]
    if len(job_zip_fnames) < 1:
        job.error = '*.zip file not found in job directory'
        return job
    if len(job_zip_fnames) > 1:
        job.error = 'Multiple *.zip files found in job directory'
        return job
    job_zip = SimpleZipFile(str(job_zip_fnames[0]))
    if not job_zip.is_valid():
        job.error = f'{job_zip_fnames[0]} is invalid: {job_zip.error}'
        return job
    if not job_zip.has_name('job.ini'):
        job.error = f'"job.ini" not found in {job_zip_fnames[0]}'
        return job
    job_ini_contents = job_zip.get_contents('job.ini')
    cp = configparser.ConfigParser()
    cp.read_string(job_ini_contents, source='job.ini')
    if not cp.has_section('JOB'):
        job.error = f'"job.ini" is missing section "JOB"'
        return job
    job.title = cp.get('JOB', 'title', fallback='(none)')
    job.handler = cp.get('JOB', 'handler', fallback='(none)')
    job.dt_created = str(cp.get('JOB', 'created', fallback='(none)')).partition('.')[0]
    job.comments = cp.get('JOB', 'comments', fallback='(none)')

    # ---- From job-run.ini
    jobrun_file = job_dir / 'job-run.ini'
    if not jobrun_file.exists():
        job.status = 'uploaded'
    else:
        cp = configparser.ConfigParser()
        cp.read(str(jobrun_file))
        if not cp.has_section('JOB'):
            job.error = f'"job-run.ini" is missing section "JOB"'
            return job
        job.status = cp.get('JOB', 'status', fallback='(missing)')
        job.dt_uploaded = cp.get('JOB', 'dt_uploaded', fallback='(missing)')
        # job.dt_last = cp.get('JOB', 'dt_last', fallback='(missing)')  # NOT USED ANYMORE

    # ---- Extra
    if details > 0:
        joblog_file = job_dir / 'job.log'
        if not joblog_file.exists():
            job.log = '(job log is missing)'
            return job
        with open(str(joblog_file), mode='rb') as f:
            job.log = f.read().decode(encoding='utf8')

    return job
