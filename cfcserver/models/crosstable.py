
from dataclasses import dataclass, field, asdict


@dataclass
class CrosstableEntry:
    # ---- Tournament
    t_id: int
    name: str
    last_day: str
    prov: str
    type: str
    # ---- Crosstable Entry
    place: int
    m_id: int
    results: str
    score: float
    games_played: int
    rating_pre: int
    rating_perf: int
    rating_post: int
    rating_hi: int
    m_name: str = field(default='')

    def __post_init__(self):
        pass

    def asdict(self):
        return asdict(self)
