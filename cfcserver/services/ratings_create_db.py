# ======================================================================
# services/ratings_create_db.py
#   - Create ratings database (SQLite) from a "job-file" (a .zip file
#     containing a job.ini and member & event data files).
#   - The job-file is created by CFC-Tools and uploaded to CFC-Server.
# ======================================================================
import os, sys, csv, logging
from pathlib import Path
from cfcserver import AppConfig
from ..dao import ratings2 as dao_ratings
from ..dao import job

log: logging.Logger

def create(job_dir):
    okay, job_dir = _initialize(job_dir)
    with AppConfig.RATINGS_DB(open_next_version=True) as db:
        if okay:
            okay = _create_new_database_and_tables(db)
        if okay:
            okay = _insert_metadata(db, job_dir)
        if okay:
            okay = _insert_members(db, job_dir)
        if okay:
            okay = _insert_historical_events(db)
        if okay:
            okay = _insert_recent_events(db, job_dir)
        if okay:
            okay = _create_indices(db)
        if okay:
            okay = _create_extract_for_ratings_audit(db)
        if okay:
            db.make_this_db_active()
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
    log.info('JOB STARTED: Creating the next Ratings Database:')
    log.info('Job directory: %s', job_dir)
    return True, job_dir


def _create_new_database_and_tables(db):
    log.info('Creating database tables:')
    dao_ratings.create_tables(db)
    log.info('... Database name: %s', getattr(db.db_fpath, 'name', '(undefined)'))
    return True


def _insert_metadata(db, job_dir):
    log.info('Loading metadata:')
    job_config = job.JobConfig.from_job_dir(job_dir)
    text4web = '...'
    if job_config.has_section('ARGS') and 'updated_text' in job_config['ARGS']:
        text4web = job_config['ARGS']['updated_text']
    log.info('... setting updated_text to "%s"', text4web)
    metadata = {'updated_text': text4web}
    dao_ratings.insert_metadata(db, metadata)
    log.info('... DONE!')
    return True


def _insert_members(db, job_dir):
    log.info('Loading member data:')
    log.info('... directory: %s', job_dir)
    for data_fp in job_dir.glob('members.*.csv'):
        n = dao_ratings.load_members_from_csv(db, data_fp)
        log.info(f'... loaded data from {data_fp.name} ({n:,})')
    log.info('... DONE!')
    return True


def _insert_historical_events(db):
    historical_dir = Path(db.db_directory, 'historical').resolve()
    log.info('Loading historical events data:')
    log.info('... directory: %s', historical_dir)
    for data_fp in historical_dir.glob('ratings.*.events.csv'):
        n = dao_ratings.load_events_from_csv(db, data_fp)
        log.info(f'... loaded data from {data_fp.name} ({n:,})')
    for data_fp in historical_dir.glob('ratings.*.results.csv'):
        n = dao_ratings.load_results_from_csv(db, data_fp)
        log.info(f'... loaded data from {data_fp.name} ({n:,})')
    log.info('... DONE!')
    return True


def _insert_recent_events(db, job_dir):
    log.info('Loading recent events data:')
    log.info('... directory: %s', job_dir)
    for data_fp in job_dir.glob('ratings.*.events.csv'):
        n = dao_ratings.load_events_from_csv(db, data_fp)
        log.info(f'... loaded data from {data_fp.name} ({n:,})')
    for data_fp in job_dir.glob('ratings.*.results.csv'):
        n = dao_ratings.load_results_from_csv(db, data_fp)
        log.info(f'... loaded data from {data_fp.name} ({n:,})')
    log.info('... DONE!')
    return True


def _create_indices(db):
    log.info('Creating database indices:')
    db.execute('CREATE INDEX ix_player_1 ON player (m_id)')
    db.execute('CREATE INDEX ix_player_2 ON player (last_lc, first_lc)')
    db.execute('CREATE INDEX ix_tournament_1 ON tournament (t_id)')
    db.execute('CREATE INDEX ix_crosstable_1 ON crosstable (t_id, place)')
    db.execute('CREATE INDEX ix_crosstable_2 ON crosstable (m_id)')
    db.commit()
    return True


def _create_extract_for_ratings_audit(db):
    return True


def _activate_database(db):
    return True
