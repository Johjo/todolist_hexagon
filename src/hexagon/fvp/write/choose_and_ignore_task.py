from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import FinalVersionPerfectedSession, FvpSessionSetPort
from src.hexagon.shared.type import TaskKey, UserKey


class ChooseAndIgnoreTaskFvp:
    def __init__(self, set_of_fvp_sessions: FvpSessionSetPort):
        self.set_of_fvp_sessions = set_of_fvp_sessions

    def execute(self, user_key: UserKey, chosen_task_id: TaskKey, ignored_task_id: TaskKey):
        session = self._get_or_create_session(user_key=user_key)

        session.choose_and_ignore_task(chosen_task_id, ignored_task_id)

        self._save(user_key=user_key, session=session)

    def _save(self, user_key: UserKey, session: FinalVersionPerfectedSession):
        snapshot = session.to_snapshot()
        self.set_of_fvp_sessions.save(user_key=user_key, snapshot=snapshot)

    def _get_or_create_session(self, user_key: UserKey):
        snapshot = self.set_of_fvp_sessions.by(user_key=user_key)
        if snapshot:
            session = FinalVersionPerfectedSession.from_snapshot(snapshot)
        else:
            raise NotImplementedError()
        return session

    @classmethod
    def factory(cls, dependencies : Dependencies) -> 'ChooseAndIgnoreTaskFvp':
        return ChooseAndIgnoreTaskFvp(set_of_fvp_sessions=dependencies.get_adapter(FvpSessionSetPort))
