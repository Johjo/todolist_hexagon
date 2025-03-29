from typing import OrderedDict

import pytest

from tests.todolist_hexagon.adapter_dependencies_for_test import AdapterDependenciesForTest
from tests.todolist_hexagon.fvp.write.fixture import FvpSessionSetForTest
from todolist_hexagon.builder import a_task_key
from todolist_hexagon.fvp.aggregate import FvpSnapshot
from todolist_hexagon.shared.type import TaskKey, UserKey
from todolist_hexagon.use_case_dependencies import UseCaseDependencies


@pytest.fixture
def fvp_sessions_set():
    return FvpSessionSetForTest()


@pytest.fixture
def sut(fvp_sessions_set):
    return UseCaseDependencies(AdapterDependenciesForTest(fvp_session_set=fvp_sessions_set)).choose_and_ignore_task()



def test_should_choose_and_ignore_when_no_task_already_chosen(sut, fvp_sessions_set):
    user_key = UserKey("the user")
    sut.execute(user_key=user_key, chosen_task_id=a_task_key(1), ignored_task_id=a_task_key(2))
    assert fvp_sessions_set.by(user_key=user_key) == FvpSnapshot(OrderedDict[TaskKey, TaskKey]({a_task_key(2): a_task_key(1)}))


def test_should_choose_and_ignore_when_one_task_already_chosen(sut, fvp_sessions_set):
    user_key = UserKey("the user")
    fvp_sessions_set.feed(user_key=user_key, snapshot=FvpSnapshot(OrderedDict[TaskKey, TaskKey]({a_task_key(2): a_task_key(1)})))

    sut.execute(user_key=user_key, chosen_task_id=a_task_key(1), ignored_task_id=a_task_key(3))

    assert fvp_sessions_set.by(user_key=user_key) == FvpSnapshot(
        OrderedDict[TaskKey, TaskKey]({a_task_key(2): a_task_key(1), a_task_key(3): a_task_key(1)}))


