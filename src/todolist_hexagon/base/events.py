from dataclasses import dataclass
from datetime import datetime
from typing import TypeVar


@dataclass(frozen=True)
class EventBase:
    when: datetime


ET = TypeVar('ET', bound=EventBase)
EventList = list[ET]
