import flask
import cfcserver.services.jobs as s_jobs
from .auth import auth


def list():
    jobs_list = s_jobs.jobs_list()
    return flask.render_template('jobs/list.html', vm=locals())


def upload():
    return flask.render_template('under-construction.html')


def view(job_name):
    return flask.render_template('under-construction.html')
