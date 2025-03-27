from typing import OrderedDict

import pytest

from src.hexagon.shared.type import TaskKey, UserKey
from tests.fixture import a_task_key
from src.hexagon.fvp.aggregate import FvpSnapshot
from src.hexagon.fvp.write.choose_and_ignore_task import ChooseAndIgnoreTaskFvp
from tests.hexagon.fvp.write.fixture import FvpSessionSetForTest


@pytest.fixture
def fvp_sessions_set():
    return FvpSessionSetForTest()


@pytest.fixture
def sut(fvp_sessions_set):
    return ChooseAndIgnoreTaskFvp(fvp_sessions_set)


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


