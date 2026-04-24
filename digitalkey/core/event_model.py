from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any


@dataclass
class Event:
    timestamp: datetime
    level: str
    module: str
    message: str
    attributes: Dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default=None):
        return self.attributes.get(key, default)

    def has(self, key: str) -> bool:
        return key in self.attributes
