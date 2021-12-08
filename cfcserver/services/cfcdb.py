
import sys, logging
from pathlib import Path
from cfcserver import AppConfig
from cfcserver.gateways import ds_job
from cfcserver.gateways import ds_cfcdb

log: logging.Logger


def create(job_dir):
    next_version = AppConfig.CFCDB.get_next_unused_version()
    with AppConfig.CFCDB.connect(version=next_version) as dbcon:
        job_dir = _initialize(job_dir)
        _create_new_database_and_tables(dbcon)
        _insert_metadata(dbcon, job_dir)
        _insert_members(dbcon, job_dir)
        _insert_historical_events(dbcon)
        _insert_recent_events(dbcon, job_dir)
        _create_indices(dbcon)
        _set_active_version(next_version)
    with AppConfig.CFCDB.connect() as dbcon:
        _create_ratings_audit_file(dbcon)
    log.info('JOB ENDED:')


def _initialize(job_dir):
    global log
    job_dir = Path(AppConfig.JOBS_DIR, job_dir).resolve()
    if not job_dir.exists():
        sys.exit(f'ERROR: Job directory not found: {job_dir}')

    log = logging.getLogger(str(job_dir))
    log.setLevel(logging.INFO)
    log_format = logging.Formatter('%(asctime)s: %(message)s', datefmt='%Y-%m-%d-%H:%M:%S')
    log_handler = logging.FileHandler(str(Path(job_dir, 'job.log')))
    log_handler.setFormatter(log_format)
    log.addHandler(log_handler)

    log.info('---- ' * 10)
    log.info('JOB STARTED: Creating the next "cfcdb" database:')
    log.info('Job directory: %s', job_dir)
    return job_dir


def _create_new_database_and_tables(dbcon):
    log.info('Creating database tables:')
    ds_cfcdb.create_tables(dbcon)


def _insert_metadata(dbcon, job_dir):
    log.info('Loading metadata:')
    job_config = ds_job.JobConfig.from_job_dir(job_dir)
    text4web = '...'
    if job_config.has_section('ARGS') and 'updated_text' in job_config['ARGS']:
        text4web = job_config['ARGS']['updated_text']
    log.info('... setting updated_text to "%s"', text4web)
    metadata = {'updated_text': text4web}
    ds_cfcdb.metadata_insert(dbcon, metadata)


def _insert_members(dbcon, job_dir):
    log.info('Loading member data:')
    log.info('... directory: %s', job_dir)
    total_loaded = 0
    for data_fp in job_dir.glob('members.*.csv'):
        n = ds_cfcdb.members_load_from_csv(dbcon, data_fp)
        log.info(f'... loaded data from {data_fp.name} ({n:,})')
        total_loaded += n
    log.info(f'... {total_loaded:,} members were loaded.')


def _insert_historical_events(dbcon):
    historical_dir = Path(AppConfig.CFCDB.directory, 'historical').resolve()
    log.info('Loading historical events data:')
    log.info('... directory: %s', historical_dir)
    total_loaded = 0
    for data_fp in historical_dir.glob('ratings.*.events.csv'):
        n = ds_cfcdb.events_load_from_csv(dbcon, data_fp)
        log.info(f'... loaded data from {data_fp.name} ({n:,})')
        total_loaded += n
    log.info(f'... {total_loaded:,} historical events were loaded.')

    log.info('Loading historical results data:')
    total_loaded = 0
    for data_fp in historical_dir.glob('ratings.*.results.csv'):
        n = ds_cfcdb.results_load_from_csv(dbcon, data_fp)
        log.info(f'... loaded data from {data_fp.name} ({n:,})')
        total_loaded += n
    log.info(f'... {total_loaded:,} historical results were loaded.')


def _insert_recent_events(dbcon, job_dir):
    log.info('Loading recent events data:')
    log.info('... directory: %s', job_dir)
    total_loaded = 0
    for data_fp in job_dir.glob('ratings.*.events.csv'):
        n = ds_cfcdb.events_load_from_csv(dbcon, data_fp)
        log.info(f'... loaded data from {data_fp.name} ({n:,})')
        total_loaded += n
    log.info(f'... {total_loaded:,} recent events were loaded.')

    log.info('Loading recent results data:')
    total_loaded = 0
    for data_fp in job_dir.glob('ratings.*.results.csv'):
        n = ds_cfcdb.results_load_from_csv(dbcon, data_fp)
        log.info(f'... loaded data from {data_fp.name} ({n:,})')
        total_loaded += n
    log.info(f'... {total_loaded:,} recent results were loaded.')


def _create_indices(dbcon):
    log.info('Creating database indices:')
    ds_cfcdb.create_indices(dbcon)


def _set_active_version(next_version):
    log.info('Setting active database version to %04d', next_version)
    AppConfig.CFCDB.set_active_version(next_version)


def _create_ratings_audit_file(dbcon):
    # log.info('Creating Ratings Audit file')
    pass
