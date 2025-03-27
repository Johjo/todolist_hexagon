from collections import OrderedDict

from src.hexagon.fvp.aggregate import FvpSessionSetPort, FvpSnapshot
from src.hexagon.shared.type import TaskKey, UserKey


class FvpSessionSetForTest(FvpSessionSetPort):
    def __init__(self) -> None:
        self.snapshot: dict[UserKey, FvpSnapshot] = {}

    def save(self, user_key: UserKey, snapshot: FvpSnapshot) -> None:
        self.snapshot[user_key] = snapshot

    def by(self, user_key: UserKey) -> FvpSnapshot:
        if user_key not in self.snapshot:
            return FvpSnapshot(OrderedDict[TaskKey, TaskKey]())
        return self.snapshot[user_key]

    def feed(self, user_key: UserKey, snapshot: FvpSnapshot) -> None:
        self.snapshot[user_key] = snapshot
