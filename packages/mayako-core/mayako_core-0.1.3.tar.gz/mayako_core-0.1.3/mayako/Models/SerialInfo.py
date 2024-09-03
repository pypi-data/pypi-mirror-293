from dataclasses import dataclass, asdict
from typing import Dict, Self

@dataclass
class SerialInfo:
    port: str
    serial_number: str
    description: str

    def format_string(self) -> str:
        return f"Port: {self.port} -- Serial Number: {self.serial_number}"
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> Self:
        return cls(**data)