from dataclasses import replace

import pytest
from expression import Ok, Error

from todolist_hexagon.todolist.write.close_task import CloseTaskUseCase
from use_case_dependencies import UseCaseDependencies
from tests.fixture import TodolistFaker
from tests.todolist_hexagon.todolist.fixture import TodolistSetForTest
from tests.todolist_hexagon.adapter_dependencies_for_test import AdapterDependenciesForTest


@pytest.fixture
def sut(todolist_set: TodolistSetForTest):
    return UseCaseDependencies(AdapterDependenciesForTest(todolist_set)).close_task()


def test_close_task(sut: CloseTaskUseCase, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    task = fake.a_task()
    todolist = fake.a_todolist().having(tasks=[task])
    todolist_set.feed(todolist)

    sut.execute(todolist_key=todolist.to_key(), task_key=task.to_key())

    actual = todolist_set.by(todolist.to_key()).value
    assert actual == todolist.having(tasks=[task.having(is_open=False)]).to_snapshot()


def test_close_when_two_tasks(sut: CloseTaskUseCase, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    first_task = fake.a_task(1)
    closed_task = fake.a_task(2)
    todolist = fake.a_todolist().having(tasks=[first_task, closed_task])
    todolist_set.feed(todolist)

    sut.execute(todolist_key=todolist.to_key(), task_key=closed_task.to_key())

    actual = todolist_set.by(todolist_key=todolist.to_key()).value
    assert actual == todolist.having(tasks=[first_task, (replace(closed_task, is_open=False))]).to_snapshot()


def test_tell_ok_when_close_task(sut: CloseTaskUseCase, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    task = fake.a_task()
    todolist = fake.a_todolist().having(tasks=[task])
    todolist_set.feed(todolist)

    response = sut.execute(todolist_key=todolist.to_key(), task_key=task.to_key())

    assert response == Ok(None)


def test_tell_error_if_task_does_not_exist(sut: CloseTaskUseCase, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    todolist = fake.a_todolist()
    todolist_set.feed(todolist)

    task = fake.a_task()
    response = sut.execute(todolist_key=todolist.to_key(), task_key=task.to_key())

    assert response == Error(f"The task '{task.to_key()}' does not exist")
