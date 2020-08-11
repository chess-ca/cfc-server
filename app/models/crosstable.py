
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
    m_name: str
    results: str
    score: float
    games_played: int
    rating_pre: int
    rating_perf: int
    rating_post: int
    rating_hi: int

    def __post_init__(self):
        pass

    def asdict(self):
        return asdict(self)
