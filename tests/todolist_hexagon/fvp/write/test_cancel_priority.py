import pytest

from tests.todolist_hexagon.adapter_dependencies_for_test import AdapterDependenciesForTest
from tests.todolist_hexagon.fvp.write.fixture import FvpSessionSetForTest
from todolist_hexagon.builder import a_task_key
from todolist_hexagon.fvp.aggregate import FvpSnapshot
from todolist_hexagon.fvp.write.cancel_priority import CancelPriority
from todolist_hexagon.shared.type import UserKey
from use_case_dependencies import UseCaseDependencies


@pytest.fixture
def session_set():
    return FvpSessionSetForTest()


@pytest.fixture
def sut(session_set: FvpSessionSetForTest):
    return UseCaseDependencies(AdapterDependenciesForTest(fvp_session_set=session_set)).cancel_priority()


def test_remove_priority_when_only_one(sut: CancelPriority, session_set: FvpSessionSetForTest):
    user_key = UserKey("the user")
    session_set.feed(user_key=user_key, snapshot=FvpSnapshot.from_primitive_dict({a_task_key(2): a_task_key(1)}))

    sut.execute(user_key=user_key, task_key=a_task_key(1))

    assert session_set.by(user_key=user_key) == FvpSnapshot.from_primitive_dict({})


def test_cancel_priority_when_one_task(sut: CancelPriority, session_set: FvpSessionSetForTest):
    user_key = UserKey("the user")
    session_set.feed(user_key=user_key, snapshot=FvpSnapshot.from_primitive_dict({a_task_key(1): a_task_key(2), a_task_key(2): a_task_key(3)}))

    sut.execute(user_key=user_key, task_key=a_task_key(3))

    assert session_set.by(user_key=user_key) == FvpSnapshot.from_primitive_dict({a_task_key(1): a_task_key(2)})

def test_cancel_priority_when_many_links(sut: CancelPriority, session_set: FvpSessionSetForTest):
    user_key = UserKey("the user")
    session_set.feed(user_key=user_key, snapshot=FvpSnapshot.from_primitive_dict({a_task_key(1): a_task_key(2), a_task_key(3): a_task_key(2)}))

    sut.execute(user_key=user_key, task_key=a_task_key(2))

    assert session_set.by(user_key) == FvpSnapshot.from_primitive_dict({})
