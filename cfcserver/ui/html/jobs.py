import datetime, pytz
from pathlib import Path
import flask
from werkzeug.utils import secure_filename
import cfcserver.services.jobs as s_jobs
from .auth import auth
from .utils import render_svelte
from cfcserver.models.appconfig import AppConfig

_tz_eastern = pytz.timezone('Canada/Eastern')


@auth
def job_list():
    job_list = sorted(
        s_jobs.jobs_list(),
        key=lambda j: j.uts_last, reverse=True
    )
    vm = {'job_list': job_list}
    return render_svelte('JobList', vm)


@auth
def job_upload():
    return render_svelte('JobUpload')


@auth(api=True)
def job_upload_post():
    req = flask.request
    if 'upload_file' not in req.files:
        flask.abort(flask.Response('"upload_file" is not in request.files', status=400))
    upload_file = flask.request.files['upload_file']
    if not upload_file.filename:
        flask.abort(flask.Response('Upload file is missing a filename', status=400))
    jobs_dir = Path(AppConfig.JOBS_DIR)
    job_filename = Path(secure_filename(upload_file.filename))
    i = 0
    job_dir = jobs_dir / job_filename.stem
    while job_dir.exists():
        i += 1
        job_dir = jobs_dir / f'{job_filename.stem}.{i:0>2}'
    job_dir.mkdir()
    upload_file.save(str(job_dir / job_filename))

    with open(str(job_dir / 'job-run.ini'), 'at') as ini:
        ini.write(f'[JOB]\nstatus = uploaded\n'
            + 'run_type = extract-from-cfc-mdb\n'
            + 'run_after = 0000-00-00-00:00:00\n'
            + 'run_attempts = 0\n')
    with open(str(job_dir / 'job.log'), 'at') as log:
        now = datetime.datetime.now(tz=_tz_eastern).strftime('%Y-%m-%d-%H:%M:%S')
        log.write(f'{now}: Job "{str(job_filename)}" uploaded and saved.\n')
    rsp = flask.make_response(dict(apicode=0, errors=[]))
    return rsp


@auth
def job_view(job_name):
    return render_svelte('UnderConstruction')
