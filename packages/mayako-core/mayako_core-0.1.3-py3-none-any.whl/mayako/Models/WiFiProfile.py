from dataclasses import dataclass, asdict
from typing import Self, Dict

@dataclass
class WiFiProfile():
    wifi_key: str
    ssid: str
    password: str
    client_ip: str
    client_port: int

    def format_string(self) -> str:
        return f"WiFi Key: {self.wifi_key} -- SSID: {self.ssid} -- client IP: {self.client_ip} -- client Port: {self.client_port}"
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> Self:
        return cls(**data)