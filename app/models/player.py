
from dataclasses import dataclass, field, asdict


@dataclass
class Player:
    m_id: int
    fide_id: int
    expiry: str
    first: str
    last: str
    city: str
    prov: str
    sex: str
    birthdate: str
    rating: int
    rating_hi: int
    quick: int
    quick_hi: int
    name: str = field(init=False)
    city_prov: str = field(init=False)
    tournaments: list = field(init=False, default=None)

    def __post_init__(self):
        self.name = f'{self.last}, {self.first}'
        self.city_prov = self.city if self.prov == 'FO' \
            else self.prov if not self.city \
            else f'{self.city}, {self.prov}'

    def asdict(self):
        return asdict(self)
