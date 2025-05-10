from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic
from uuid import UUID

from todolist_hexagon.events import Event
from todolist_hexagon.base.events import EventList, ET


@dataclass
class AggregateEvent(Generic[ET]):
    key: UUID
    events: EventList[ET]

class EventStorePort(ABC, Generic[ET]):
    @abstractmethod
    def save(self, *aggregate_events: AggregateEvent[ET]) -> None:
        pass

    @abstractmethod
    def events_for(self, key: UUID) -> EventList[ET]:
        pass
