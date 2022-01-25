# ======================================================================
# cfcdb schema:
#   - Indices are not defined in the schema since they should be created
#     *after* all the data has been bulk-loaded.  Use create_indices().
# ======================================================================
from sqlalchemy import *

sa_metadata = MetaData()

t_metadata = Table('metadata', sa_metadata,
    Column('key', String(), primary_key=True),
    Column('value', String(100)),
)

t_player = Table('player', sa_metadata,
    Column('cfc_id', Integer, primary_key=True),
    Column('cfc_expiry', String(10)),
    Column('cfc_type', String(20)),
    Column('gomembership_id', String(50)),
    Column('fide_id', Integer, default=0),
    Column('name_first', String(50)),
    Column('name_last', String(50)),
    Column('birthdate', String(10)),
    Column('gender', String(1), default=''),
    Column('email', String(50), default=''),
    Column('phone', String(50), default=''),
    Column('addr_line1', String(50), default=''),
    Column('addr_line2', String(50), default=''),
    Column('addr_city', String(50), default=''),
    Column('addr_province', String(50), default=''),
    Column('addr_postalcode', String(20), default=''),
    Column('regular_rating', Integer, default=0),
    Column('regular_indicator', Integer, default=0),
    Column('quick_rating', Integer, default=0),
    Column('quick_indicator', Integer, default=0),
    Column('notes', String(10000), default=''),
    Column('last_udpate', String(10), default=''),
    Column('name_first_lc', String(50)),                # ??? not if can query case-insensitive?
    Column('name_last_lc', String(50)),
)

t_event = Table('event', sa_metadata,
    Column('id', Integer),
    Column('name', String(100)),
    Column('date_end', String(10)),
    Column('province', String(50)),
    Column('organizer_id', Integer, ForeignKey('player.cfc_id')),
    Column('arbiter_id', Integer, ForeignKey('player.cfc_id')),
    Column('pairings', String(20)),         # SS|RR
    Column('rating_type', String(20)),      # R|Q
    Column('n_players', Integer),
    Column('n_rounds', Integer),
)

t_crosstable = Table('crosstable', sa_metadata,
    Column('event_id', Integer, ForeignKey('event.id')),
    Column('place', Integer),
    Column('cfc_id', Integer, ForeignKey('player.cfc_id')),
    Column('province', String()),
    Column('games_played', Integer),
    Column('score', Float()),
    Column('results', String()),
    Column('rating_type', String()),
    Column('rating_pre', Integer),
    Column('rating_perf', Integer),
    Column('rating_post', Integer),
    Column('rating_indicator', Integer),
)


def create_indices(dbcon):
    indices = (
        Index('ix_player_1', t_player.c.cfc_id),
        Index('ix_player_2', t_player.c.name_last_lc, t_player.c.name_first_lc),
        Index('ix_event_1', t_event.c.id),
        Index('ix_event_2', t_event.c.organizer_id),
        Index('ix_event_3', t_event.c.arbiter_id),
        Index('ix_crosstable_1', t_crosstable.c.event_id, t_crosstable.c.place),
        Index('ix_crosstable_2', t_crosstable.c.cfc_id),
    )
    for index in indices:
        index.create(dbcon)
