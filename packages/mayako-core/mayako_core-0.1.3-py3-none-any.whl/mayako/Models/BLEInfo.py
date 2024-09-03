from dataclasses import dataclass, asdict
from typing import List, Dict, Self

@dataclass
class BLEInfo:
    address: str
    name: str
    service_uuids: List[str]

    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> Self:
        return cls(**data)