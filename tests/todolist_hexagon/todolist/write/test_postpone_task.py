from datetime import datetime

import pytest
from expression import Ok, Error, Some

from todolist_hexagon.shared.type import TaskExecutionDate
from todolist_hexagon.todolist.write.postpone_task import PostPoneTask
from todolist_hexagon.use_case_dependencies import UseCaseDependencies

from todolist_hexagon.builder import TodolistFaker
from tests.todolist_hexagon.todolist.fixture import TodolistSetForTest
from tests.todolist_hexagon.read_adapter_dependencies_for_test import ReadAdapterDependenciesForTest
from tests.todolist_hexagon.write_adapter_dependencies_for_test import WriteAdapterDependenciesForTest


@pytest.fixture
def sut(todolist_set: TodolistSetForTest) -> PostPoneTask:
    return UseCaseDependencies(WriteAdapterDependenciesForTest(todolist_set=todolist_set)).postpone_task()


def test_save_postponed_task(sut: PostPoneTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    task = fake.a_task()
    todolist = fake.a_todolist().having(tasks=(task,))
    todolist_set.feed(todolist)

    today = datetime.today()
    sut.execute(todolist_key=todolist.to_key(), key=task.to_key(), execution_date=TaskExecutionDate(today))

    actual = todolist_set.by(todolist_key=todolist.to_key()).value
    assert actual == todolist.having(tasks=(task.having(execution_date=Some(TaskExecutionDate(today))),)).to_snapshot()


def test_postpone_task_when_two_tasks(sut: PostPoneTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    task_1 = fake.a_task()
    task_2 = fake.a_task()
    postponed_task = fake.a_task()

    todolist = fake.a_todolist().having(tasks=[task_1, postponed_task, task_2])
    todolist_set.feed(todolist)

    today = TaskExecutionDate(datetime.today())
    sut.execute(todolist_key=todolist.to_key(), key=postponed_task.to_key(), execution_date=today)

    actual = todolist_set.by(todolist_key=todolist.to_key()).value
    assert actual == todolist.having(
        tasks=[task_1, postponed_task.having(execution_date=Some(today)), task_2]).to_snapshot()


def test_tell_ok_when_postpone_task(sut: PostPoneTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    task = fake.a_task()
    todolist = fake.a_todolist().having(tasks=[task])
    todolist_set.feed(todolist)

    execution_date = fake.a_date()
    response = sut.execute(todolist_key=todolist.to_key(), key=task.to_key(), execution_date=TaskExecutionDate(execution_date))

    assert response == Ok(None)


def test_tell_error_when_task_not_found(sut: PostPoneTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    unknown_task = fake.a_task()
    todolist = fake.a_todolist()
    todolist_set.feed(todolist)

    today = datetime.today()
    response = sut.execute(todolist_key=todolist.to_key(), key=unknown_task.to_key(), execution_date=TaskExecutionDate(today))

    assert response == Error(f"The task '{unknown_task.to_key()}' does not exist")