from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from todolist_hexagon.events import EventList


@dataclass
class AggregateEvent:
    key: UUID
    events: EventList

class EventStorePort(ABC):
    @abstractmethod
    def save(self, *aggregate_event: AggregateEvent) -> None:
        pass

    @abstractmethod
    def events_for(self, key: UUID) -> EventList:
        pass
