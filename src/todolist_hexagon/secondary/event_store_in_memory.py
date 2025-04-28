from uuid import UUID

from todolist_hexagon.events import EventList
from todolist_hexagon.ports import EventStorePort, AggregateEvent


class EventStoreInMemory(EventStorePort):
    def __init__(self) -> None:
        self.events : dict[UUID, EventList] = {}

    def save(self, *aggregate_events: AggregateEvent) -> None:
        for truc in aggregate_events:
            self.events.setdefault(truc.key, [])
            self.events[truc.key].extend(truc.events)

    def events_for(self, key: UUID) -> EventList:
        return self.events.get(key, [])
