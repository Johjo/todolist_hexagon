from uuid import UUID

from events import EventList
from ports import EventStore


class EventStoreForTest(EventStore):
    def __init__(self) -> None:
        self.all_events: EventList = []
        self.events: dict[UUID, EventList] = {}

    def save(self, key: UUID, events: EventList) -> None:
        self.all_events.extend(events)
        self.events[key] = events

    def events_for(self, key: UUID) -> EventList:
        return self.events.get(key, [])
