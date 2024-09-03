from dataclasses import dataclass

@dataclass
class Battery:
    percentage: int
    charging: bool