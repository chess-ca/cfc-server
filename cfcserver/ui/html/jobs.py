import flask
import cfcserver.services.jobs as s_jobs
from .auth import auth
from .utils import render_svelte


@auth
def job_list():
    vm = {'job_list': s_jobs.jobs_list()}
    return render_svelte('JobList', vm)


@auth
def job_upload():
    return render_svelte('UnderConstruction')


@auth
def job_view(job_name):
    return render_svelte('UnderConstruction')
