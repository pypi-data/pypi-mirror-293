from dataclasses import dataclass, asdict
from typing import Dict, Self
from ..Config import CCLIENT

@dataclass
class User:
    user_mac_address: str
    arduino_folder: str = CCLIENT.DEFAULT_ARDUINO_FOLDER

    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> Self:
        return cls(**data)