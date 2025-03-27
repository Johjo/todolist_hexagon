from collections import OrderedDict

from src.hexagon.shared.type import UserKey, TaskKey
from tests.fixture import a_task_key
from src.hexagon.fvp.write.reset_fvp_session import ResetFvpSession


from src.hexagon.fvp.aggregate import FvpSnapshot
from tests.hexagon.fvp.write.fixture import FvpSessionSetForTest


def test_reset_session():
    set_of_fvp_sessions = FvpSessionSetForTest()
    user_key = UserKey("the user")
    set_of_fvp_sessions.feed(user_key=user_key, snapshot=FvpSnapshot(OrderedDict[TaskKey, TaskKey]({a_task_key(1): a_task_key(2)})))
    sut = ResetFvpSession(set_of_fvp_sessions)
    sut.execute(user_key=user_key)

    assert set_of_fvp_sessions.by(user_key=user_key) == FvpSnapshot(OrderedDict())
