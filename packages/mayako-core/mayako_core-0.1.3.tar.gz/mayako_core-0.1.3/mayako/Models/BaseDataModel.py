from abc import ABC
from dataclasses import dataclass, asdict

@dataclass
class BaseDataModel(ABC):
    """
    Source
        https://stackoverflow.com/a/2544761
    """
    timestamp: str
    sequence: int
    identity: str

    def to_dict(self, filter_none=True) -> dict:
        """
        Makes a dictionary from 
        """
        data = asdict(self)

        if filter_none:
            return {key: value for key, value in data.items() if value is not None}
        
        return data
    
    def get_class_name(self) -> str:
        return self.__class__.__name__