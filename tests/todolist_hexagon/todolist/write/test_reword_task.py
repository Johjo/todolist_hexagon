from dataclasses import replace

import pytest
from expression import Ok, Error

from todolist_hexagon.shared.type import TaskName
from todolist_hexagon.todolist.write.reword_task import RewordTask
from todolist_hexagon.use_case_dependencies import UseCaseDependencies

from todolist_hexagon.builder import TodolistFaker
from tests.todolist_hexagon.todolist.fixture import TodolistSetForTest
from tests.todolist_hexagon.write_adapter_dependencies_for_test import WriteAdapterDependenciesForTest


@pytest.fixture
def sut(todolist_set: TodolistSetForTest):
    return UseCaseDependencies(WriteAdapterDependenciesForTest(todolist_set=todolist_set)).reword_task()


def test_reword_task(sut: RewordTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    task = fake.a_task()
    todolist = fake.a_todolist().having(tasks=[task])
    todolist_set.feed(todolist)

    sut.execute(todolist_key=todolist.to_key(), task_key=task.to_key(), new_wording=TaskName("buy the milk"))

    actual = todolist_set.by(todolist_key=todolist.to_key()).value
    assert actual == todolist.having(tasks=[task.having(name="buy the milk")]).to_snapshot()


def test_reword_when_two_task(sut: RewordTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    first_task = fake.a_task(1)
    reworded_task = fake.a_task(2)
    todolist = fake.a_todolist().having(tasks=[first_task, reworded_task])
    todolist_set.feed(todolist)

    sut.execute(todolist_key=todolist.to_key(), task_key=reworded_task.to_key(), new_wording=TaskName("buy the milk"))

    actual = todolist_set.by(todolist_key=todolist.to_key()).value
    assert actual == todolist.having(tasks=[first_task, (replace(reworded_task, name="buy the milk"))]).to_snapshot()


def test_tell_ok_when_reword_task(sut: RewordTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    task = fake.a_task()
    todolist = fake.a_todolist().having(tasks=[task])
    todolist_set.feed(todolist)

    response = sut.execute(todolist_key=todolist.to_key(), task_key=task.to_key(), new_wording=TaskName("buy the milk"))

    assert response == Ok(None)


def test_tell_error_if_task_does_not_exist(sut: RewordTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    todolist = fake.a_todolist()
    todolist_set.feed(todolist)

    task = fake.a_task()
    response = sut.execute(todolist_key=todolist.to_key(), task_key=task.to_key(), new_wording=TaskName("buy the milk"))

    assert response == Error(f"The task '{task.to_key()}' does not exist")
