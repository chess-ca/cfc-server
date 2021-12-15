
from pathlib import Path
from codeboy4py.py.jobs import Job
from cfcserver import AppConfig
from cfcserver.gateways import ds_cfcdb


def create(job: Job):
    job.log('---- ' * 10)
    job.log('JOB STARTED: Creating the next "cfcdb" database:')
    job.log(f'Job directory: {job.dir}')

    next_version = AppConfig.CFCDB.get_next_unused_version()
    with AppConfig.CFCDB.connect(version=next_version) as dbcon:
        _create_new_database_and_tables(job, dbcon)
        _insert_metadata(job, dbcon)
        _insert_members(job, dbcon)
        _insert_historical_events(job, dbcon)
        _insert_recent_events(job, dbcon)
        _create_indices(job, dbcon)
        _set_active_version(job, next_version)
    with AppConfig.CFCDB.connect() as dbcon:
        _create_ratings_audit_file(job, dbcon)
    job.log('JOB ENDED:')


def _create_new_database_and_tables(job: Job, dbcon):
    job.log('Creating database tables:')
    ds_cfcdb.create_tables(dbcon)


def _insert_metadata(job: Job, dbcon):
    job.log('Loading metadata:')
    text4web = job.ini_get('ARGS', 'updated_text', default='...')
    job.log(f'... setting updated_text to "{text4web}"')
    metadata = {'updated_text': text4web}
    ds_cfcdb.metadata_insert(dbcon, metadata)


def _insert_members(job: Job, dbcon):
    job.log('Loading member data:')
    job.log(f'... directory: {job.dir}')

    total_loaded = 0
    for csv_fn, csv_fo in job.file_objects(pattern=r'members\..*?\.csv'):
        n = ds_cfcdb.members_load_from_csv_file(dbcon, csv_fo)
        job.log(f'... loaded data from {csv_fn} ({n:,})')
        total_loaded += n
    job.log(f'... {total_loaded:,} members were loaded.')


def _insert_historical_events(job: Job, dbcon):
    historical_dir = Path(AppConfig.CFCDB.directory, 'historical').resolve()
    job.log('Loading historical events data:')
    job.log(f'... directory: {historical_dir}')
    total_loaded = 0
    for data_fp in historical_dir.glob('ratings.*.events.csv'):
        with open(str(data_fp), 'rt') as csv_f:
            n = ds_cfcdb.events_load_from_csv(dbcon, csv_f)
            job.log(f'... loaded data from {data_fp.name} ({n:,})')
            total_loaded += n
    job.log(f'... {total_loaded:,} historical events were loaded.')

    job.log('Loading historical results data:')
    total_loaded = 0
    for data_fp in historical_dir.glob('ratings.*.results.csv'):
        with open(str(data_fp), 'rt') as csv_f:
            n = ds_cfcdb.results_load_from_csv(dbcon, csv_f)
            job.log(f'... loaded data from {data_fp.name} ({n:,})')
            total_loaded += n
    job.log(f'... {total_loaded:,} historical results were loaded.')


def _insert_recent_events(job: Job, dbcon):
    job.log('Loading recent events data:')
    job.log(f'... directory: {job.dir}')
    total_loaded = 0
    for csv_fn, csv_f in job.file_objects(pattern=r'ratings\..*?\.events\.csv'):
        n = ds_cfcdb.events_load_from_csv(dbcon, csv_f)
        job.log(f'... loaded data from {csv_fn} ({n:,})')
        total_loaded += n
    job.log(f'... {total_loaded:,} recent events were loaded.')

    job.log('Loading recent results data:')
    total_loaded = 0
    for csv_fn, csv_f in job.file_objects(pattern=r'ratings\..*?\.results\.csv'):
        n = ds_cfcdb.results_load_from_csv(dbcon, csv_f)
        job.log(f'... loaded data from {csv_fn} ({n:,})')
        total_loaded += n
    job.log(f'... {total_loaded:,} recent results were loaded.')


def _create_indices(job: Job, dbcon):
    job.log('Creating database indices:')
    ds_cfcdb.create_indices(dbcon)


def _set_active_version(job: Job, next_version):
    job.log(f'Setting active database version to {next_version:04d}')
    AppConfig.CFCDB.set_active_version(next_version)


# TODO: Code to create ratings audit file whenever ratings updated.
def _create_ratings_audit_file(job: Job, dbcon):
    # job.log('Creating Ratings Audit file')
    pass
