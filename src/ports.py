from abc import ABC, abstractmethod
from uuid import UUID

from src.events import EventList


class EventStore(ABC):
    @abstractmethod
    def save(self, key: UUID, events: EventList) -> None:
        pass

    @abstractmethod
    def events_for(self, key: UUID) -> EventList:
        pass
