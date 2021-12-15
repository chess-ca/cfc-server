import datetime, pytz
from pathlib import Path
import flask
from werkzeug.utils import secure_filename
from codeboy4py.py.jobs import Job
import cfcserver.services.jobs as s_jobs
from .auth import auth
from .utils import render_svelte
from cfcserver.models.appconfig import AppConfig


@auth
def job_list():
    job_list = sorted(
        s_jobs.jobs_list(),
        key=lambda j: j.updated_uts, reverse=True
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
        rsp = dict(apicode=400, errors=['"upload_file" is not in request.files'])
        return flask.make_response(rsp)
    upload_file = flask.request.files['upload_file']
    if not upload_file.filename:
        rsp = dict(apicode=400, errors=['Upload file is missing a filename'])
        return flask.make_response(rsp)
    jobs_dir = Path(AppConfig.JOBS_DIR)
    job_filename = Path(secure_filename(upload_file.filename))
    i = 0
    job_dir = jobs_dir / job_filename.stem
    while job_dir.exists():
        i += 1
        job_dir = jobs_dir / f'{job_filename.stem}.{i:0>2}'
    job_dir.mkdir(parents=True)
    upload_file.save(str(job_dir / job_filename))

    try:
        Job.unpack(job_dir, timezone=AppConfig.PYTZ_TIMEZONE, runnable=True)
    except Exception as e:
        emsg = f'{type(e)}: {e.args}'
        print(emsg)
        with open(str(job_dir / 'error.log'), 'at') as error_f:
            error_f.write(emsg + '\n')
        return flask.make_response(dict(apicode=500, errors=[emsg]))

    return flask.make_response(dict(apicode=0, errors=[]))


@auth
def job_view(job_name):
    return render_svelte('UnderConstruction')
