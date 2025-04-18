from uuid import UUID

from todolist_hexagon.events import EventList
from todolist_hexagon.ports import EventStore, AggregateEvent


class EventStoreForTest(EventStore):
    def __init__(self) -> None:
        self.events: dict[UUID, EventList] = {}

    def save(self, *aggregate_events: AggregateEvent) -> None:
        for aggregate_event in aggregate_events:
            previous_events = self.events.get(aggregate_event.key, [])
            previous_events.extend(aggregate_event.events)
            self.events[aggregate_event.key] = previous_events

    def events_for(self, key: UUID) -> EventList:
        return self.events.get(key, [])

