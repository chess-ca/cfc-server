
from dataclasses import dataclass, field, asdict


@dataclass
class Tournament:
    t_id: int
    name: str
    last_day: str
    prov: str
    rounds: int
    pairings: str
    type: str
    org_m_id: int
    org_name: str = ''  # not always needed
    place: int = 0      # if for a specific player
    crosstable: list = field(init=False, default=None)

    def asdict(self):
        return asdict(self)
