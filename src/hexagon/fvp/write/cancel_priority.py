from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import FinalVersionPerfectedSession, FvpSessionSetPort
from src.hexagon.shared.type import TaskKey, UserKey


class CancelPriority:
    def __init__(self, session_set: FvpSessionSetPort):
        self._session_set = session_set

    def execute(self, user_key: UserKey, task_key: TaskKey):
        session_snapshot = self._session_set.by(user_key)
        session = FinalVersionPerfectedSession.from_snapshot(session_snapshot)
        session.cancel_priority(task_key)

        self._session_set.save(user_key=user_key, snapshot=session.to_snapshot())

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'CancelPriority':
        return CancelPriority(dependencies.get_adapter(FvpSessionSetPort))