import re

import pytz, zipfile, configparser
from datetime import datetime, timedelta, tzinfo
from pathlib import Path
from types import SimpleNamespace

_job_info = ['dir', 'dirname', 'title', 'status', 'run_type', 'comments', 'error',
    'created_dt', 'update_dt', 'updated_uts', 'log']


class Job:
    """A job, usually to be run by a schedule such as cron.

    - Jobs are created in a .zip file and uploaded/sent to the server.
      May be created by a desktop app or another application.
    - Job .zip files contain a job.ini file.
    - Job .zip files are saved in a directory and "unpacked": the
      job.ini is extracted and a job.log file is created.
    - When running jobs, only valid/unpacked jobs are considered.
    """
    def __init__(self, job_dir, timezone='UTC'):
        """
        - NOTE: Instead of raising an Exception, invalid Jobs store the
          error in self.error.  This allows use in list comprehensions
          without breaking if an invalid job is encountered.

        :param job_dir:
        :param timezone:
        """
        self.dir: Path = Path(job_dir).resolve()
        self.timezone: str = timezone

        self.error = None
        self.status: str = '???'
        self.run_type: str = '???'
        self.run_after: str = '???'
        self.run_attempts: int = 0

        self.ini_path: Path = job_dir / 'job.ini'
        self.log_path: Path = job_dir / 'job.log'
        self.tz: tzinfo = pytz.timezone(self.timezone)

        self._cparser = None

        # ---- job directory
        if not self.dir.exists():
            self.error = f'Invalid job: directory not found: {self.dir}'
            return
        if not self.dir.is_dir():
            self.error = f'Invalid job: not a directory: {self.dir}'
            return
        self.dirname = self.dir.name

        # ---- job.log
        self.updated_dt, self.updated_uts = self.get_updated()

        # ---- *.zip
        zip_fnames = [fn for fn in self.dir.glob('*.zip')]
        if len(zip_fnames) < 1:
            self.error = f'Invalid job: *.zip file is missing: {self.dir}'
            return
        if len(zip_fnames) > 1:
            self.error = f'Invalid job: Multiple *.zip files found: {self.dir}'
            return
        self.zip_path = Path(zip_fnames[0]).resolve()

        # ---- job.ini
        if not self.ini_path.exists():
            self.error = f'Invalid job: "job.ini" not found: {self.dir}'
            return
        cp = self._get_cparser()
        if not cp.has_section('JOB'):
            self.error = f'Invalid job: "job.ini" missing "JOB" section: {self.dir}'
            return
        if not cp.has_section('RUN'):
            self.error = f'Invalid job: "job.ini" missing "RUN" section: {self.dir}'
            return
        job_section = cp['JOB']
        run_section = cp['RUN']

        self.title = job_section.get('title', '???')
        self.status = run_section.get('status', '???')
        self.run_type = run_section.get('run_type', None) \
                     or job_section.get('run_type', None) \
                     or job_section.get('handler', '???')
        self.comments = job_section.get('comments', None)
        self.created_dt = job_section.get('created', '').rsplit('.', 1)[0]

    def get_info(self, details=''):
        """Get Job info (suitable for JSON, etc)"""
        info = SimpleNamespace(**{n: None for n in _job_info})
        info.dir = str(self.dir)
        if self.error:
            info.status = 'error'
            info.error = self.error
            info.updated_dt = getattr(self, 'updated_dt', 0),
            info.updated_uts = getattr(self, 'updated_uts', 0),    # for sorting lambdas
            return info

        info.dirname = self.dirname
        info.title = self.title,
        info.status = self.status,
        info.run_type = self.run_type,
        info.comments = self.comments,
        info.created_dt = self.created_dt,
        info.updated_dt = self.updated_dt,
        info.updated_uts = self.updated_uts,
        info.log = self.get_log() if 'log' in details else None,
        return info

    @staticmethod
    def unpack(job_dir, timezone='UTC'):
        """Unpack a job from its *.zip file (after uploading).
        :param job_dir
        """
        # ---- job_dir: must exist
        job_dir = Path(job_dir).resolve()
        if not job_dir.exists():
            raise ValueError(f'Job directory not found: {job_dir}')

        # ---- job_dir/*.zip - must be only 1
        zip_fnames = [fn for fn in job_dir.glob('*.zip')]
        if len(zip_fnames) < 1:
            raise ValueError(f'Invalid job: *.zip file is missing: {job_dir}')
        if len(zip_fnames) > 1:
            raise ValueError(f'Invalid job: Multiple *.zip files found: {job_dir}')
        # self.job_zip = SimpleZipFile(str(zip_fnames[0]))
        job_zip = Path(zip_fnames[0])

        # ---- job_dir/*.zip/job.ini, job.log
        with zipfile.ZipFile(str(job_zip), mode='r') as zip_f:
            if 'job.ini' not in zip_f.namelist():
                raise ValueError(f'Invalid job: "job.ini" not found in the *.zip in {job_dir}')
            zip_f.extract('job.ini', path=str(job_dir))
            if 'job.log' in zip_f.namelist():
                zip_f.extract('job.log', path=str(job_dir))

        jobini = job_dir / 'job.ini'
        joblog = job_dir / 'job.log'

        # ---- job.ini
        cp = configparser.ConfigParser()
        cp.read(str(jobini))
        if not cp.has_section('JOB'):
            raise ValueError(f'Invalid job: "job.ini" is missing a [JOB] section ({job_dir})')

        if not cp.has_section('RUN'):
            cp.add_section('RUN')
        if not cp.has_option('RUN', 'status'):
            cp.set('RUN', 'status', 'uploaded')
        if not cp.has_option('RUN', 'run_type'):
            run_type = cp.get('JOB', 'run_type', fallback=None) \
                or cp.get('JOB', 'handler', fallback=None) \
                or 'undefined'
            cp.set('RUN', 'run_type', run_type)
        if not cp.has_option('RUN', 'run_after'):
            run_after = cp.get('JOB', 'run_after', fallback='0000-00-00-00:00:00')
            cp.set('RUN', 'run_after', run_after)
        if not cp.has_option('RUN', 'run_attempts'):
            cp.set('RUN', 'run_attempts', '0')

        with open(str(jobini), 'wt') as ini_f:
            cp.write(ini_f)

        # ---- job.log
        log = []
        if not joblog.exists():
            created = cp.get('JOB', 'created', fallback='').replace(' ', '-')
            if '.' in created:      # if fractional seconds:
                created = created[:created.rfind('.')]
            created = created.split('.', maxsplit=1)[0]  # drop fractions
            title = cp.get('JOB', 'title', fallback=None)
            comments = cp.get('JOB', 'comments', fallback=None)
            log.append(f'{created}: Job *.zip file was created\n')
            if title:
                log.append(f'{created}: Job title: {title}\n')
            if comments:
                log.append(f'{created}: {comments}\n')
        now = datetime.now(tz=pytz.timezone(timezone))
        now_ts = now.strftime('%Y-%m-%d-%H:%M:%S')
        log.append(f'{now_ts}: Job *.zip file was unpacked\n')
        with open(str(joblog), 'at') as log_f:
            log_f.writelines(log)

    def ini_get(self, section, option, default=None) -> str:
        cp = self._get_cparser()
        if not cp.has_section(section):
            return default
        return cp.get(section, option, fallback=default)

    def ini_set(self, section, option, value):
        cp = self._get_cparser()
        if not cp.has_section(section):
            cp.add_section(section)
        cp.set(section, option, str(value))

    def ini_save(self):
        if self._cparser is not None:
            with open(str(self.ini_path), 'wt') as ini_f:
                self._cparser.write(ini_f)

    def _get_cparser(self) -> configparser.ConfigParser:
        if self._cparser is None:
            self._cparser = configparser.ConfigParser()
            self._cparser.read(str(self.ini_path))
        return self._cparser

    def get_updated(self):
        if not self.log_path.exists():
            return '0000-00-00-00:00:00', 0
        log_mtime = self.log_path.stat().st_mtime
        dt = datetime.fromtimestamp(log_mtime, tz=self.tz)
        return dt.strftime('%Y-%m-%d-%H:%M:%S'), int(log_mtime)

    def log_get_contents(self) -> str:
        with open(str(self.log_path), 'rt') as log_f:
            log = log_f.read()
        return log

    def get_file_names(self, pattern=None):
        """Get list of files in the job's *.zip file"""
        with zipfile.ZipFile(str(self.zip_path), mode='r') as zip_f:
            fn_list = zip_f.namelist()
        if pattern is None:
            return fn_list
        fn_re = re.compile(pattern)
        return [fn for fn in fn_list if fn_re.match(fn)]

    def get_file_contents(self, fname, bytes=False):
        """Get contents of a file in the job's *.zip file."""
        with zipfile.ZipFile(str(self.zip_path), mode='r') as zip_f:
            if fname not in zip_f.namelist():
                return None
            f_bytes: bytes = zip_f.read(fname)
            return f_bytes if bytes \
                else f_bytes.decode('utf-8')

    def get_file_obj(self, fname):
        """Get a file-object for a file in the job's *.zip file."""
        with zipfile.ZipFile(str(self.zip_path), mode='r') as zip_f:
            if fname not in zip_f.namelist():
                return None
            f_bytes: bytes = zip_f.read(fname)
            return f_bytes if bytes \
                else f_bytes.decode('utf-8')

    def log(self, *text, sep='\n\t', ts='', add_ts=True):
        if add_ts:
            now = datetime.now(tz=self.tz)
            ts = now.strftime('%Y-%m-%d-%H:%M:%S: ')
        with open(str(self.log_path), 'at', encoding='utf-8') as log_f:
            log_f.write(ts + sep.join(text) + '\n')

    def get_log(self):
        with open(str(self.log_path), 'rt', encoding='utf-8') as log_f:
            log_contents = log_f.read()
        return log_contents