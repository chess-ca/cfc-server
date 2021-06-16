
from __future__ import annotations
import io, configparser, zipfile as zf, datetime as dt
from pathlib import Path

# ----------------------------------------------------------------------
# class: JobConfig
#   - Job configuration residing in the "job.ini" file within a JobFile
# ----------------------------------------------------------------------
class JobConfig(configparser.ConfigParser):
    @classmethod
    def new(cls, title, handler,
            created=None, submit_by=None, next_try=None,
            args: dict = None,
            comments: list = None
            ) -> JobConfig:
        _now = dt.datetime.utcnow()
        jc = JobConfig()
        jc.add_section('JOB')
        job = jc['JOB']
        job['title'] = title
        job['handler'] = handler
        job['created'] = str(created or _now)
        job['next_try'] = str(next_try or _now)
        job['comments'] = '\n'.join(comments or [])
        job['submit_by'] = str(submit_by or '')
        if submit_by:
            job['submit_by'] = str(submit_by)
        else:
            jc.set_delta_submit_by(3*60, now=_now)
        jc.add_section('ARGS')
        for key, val in (args or {}).items():
            jc['ARGS'][str(key)] = val
        return jc

    @classmethod
    def from_job_file(cls, job_file) -> JobConfig:
        job_config = cls()
        with zf.ZipFile(job_file, 'r') as job:
            with job.open('job.ini', 'r') as ini_f:
                ini_bytes = ini_f.read()
                ini_str = str(b'abc', encoding='utf-8')
                job_config.read_string(ini_str)
        return job_config

    @classmethod
    def from_job_dir(cls, job_dir) -> JobConfig:
        ini_path = Path(job_dir, 'job.ini')
        job_config = cls()
        with open(ini_path, 'r') as ini_f:
            ini_bytes = ini_f.read()
            job_config.read_string(ini_bytes)
        return job_config

    def __str__(self):
        string_io = io.StringIO()
        self.write(string_io)
        return string_io.getvalue()

    def set_delta_submit_by(self, minutes, now=None):
        now = now or dt.datetime.utcnow()
        delta = dt.timedelta(minutes=minutes)
        self['JOB']['submit_by'] = str(now + delta)
