from datetime import datetime

from todolist_hexagon.todolist_usecase import DateTimeProviderPort


class DateTimeProviderFixed(DateTimeProviderPort):
    def __init__(self) -> None:
        self._now : datetime | None = None

    def now(self) -> datetime:
        if self._now is None:
            raise RuntimeError("DateTimeProviderFixed.now() called before feed()")
        return self._now

    def feed(self, now: datetime) -> None:
        self._now = now
