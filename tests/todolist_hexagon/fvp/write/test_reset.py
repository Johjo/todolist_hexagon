from collections import OrderedDict

import pytest

from todolist_hexagon.shared.type import UserKey, TaskKey
from todolist_hexagon.use_case_dependencies import UseCaseDependencies

from todolist_hexagon.builder import a_task_key
from todolist_hexagon.fvp.write.reset_fvp_session import ResetFvpSession


from todolist_hexagon.fvp.aggregate import FvpSnapshot
from tests.todolist_hexagon.adapter_dependencies_for_test import AdapterDependenciesForTest
from tests.todolist_hexagon.fvp.write.fixture import FvpSessionSetForTest

@pytest.fixture
def sut(fvp_session_set: FvpSessionSetForTest):
    return UseCaseDependencies(AdapterDependenciesForTest(fvp_session_set=fvp_session_set)).reset_fvp_session()


def test_reset_session():
    set_of_fvp_sessions = FvpSessionSetForTest()
    user_key = UserKey("the user")
    set_of_fvp_sessions.feed(user_key=user_key, snapshot=FvpSnapshot(OrderedDict[TaskKey, TaskKey]({a_task_key(1): a_task_key(2)})))
    sut = ResetFvpSession(set_of_fvp_sessions)
    sut.execute(user_key=user_key)

    assert set_of_fvp_sessions.by(user_key=user_key) == FvpSnapshot(OrderedDict())
