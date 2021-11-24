import flask
import cfcserver.services.jobs as s_jobs
from .auth import auth
from .utils import render_svelte


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
    return render_svelte('UnderConstruction')


@auth
def job_view(job_name):
    return render_svelte('UnderConstruction')
