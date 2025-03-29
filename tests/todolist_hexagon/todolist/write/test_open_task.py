import pytest
from expression import Ok, Error

from todolist_hexagon.use_case_dependencies import UseCaseDependencies

from todolist_hexagon.builder import TodolistFaker
from tests.todolist_hexagon.todolist.fixture import TaskKeyGeneratorForTest, TodolistSetForTest

from todolist_hexagon.todolist.write.open_task import OpenTaskUseCase
from tests.todolist_hexagon.adapter_dependencies_for_test import AdapterDependenciesForTest


@pytest.fixture
def task_key_generator() -> TaskKeyGeneratorForTest:
    return TaskKeyGeneratorForTest()


@pytest.fixture
def sut(todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest) -> OpenTaskUseCase:
    return UseCaseDependencies(AdapterDependenciesForTest(todolist_set=todolist_set, task_key_generator=task_key_generator)).open_task()


def test_open_task_when_no_task(sut: OpenTaskUseCase, todolist_set: TodolistSetForTest,
                                task_key_generator: TaskKeyGeneratorForTest, fake: TodolistFaker):
    todolist = fake.a_todolist()
    todolist_set.feed(todolist)
    expected_task = fake.a_task()

    task_key_generator.feed(expected_task.to_key())

    sut.execute(todolist_key=todolist.to_key(), task_key=expected_task.to_key(), name=expected_task.to_name())

    actual = todolist_set.by(todolist_key=todolist.to_key()).value

    assert actual == todolist.having(tasks=[expected_task]).to_snapshot()


def test_open_task_when_one_task(sut, todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest,
                                 fake: TodolistFaker):
    first_task = fake.a_task(1)
    expected_task = fake.a_task(2)

    todolist = fake.a_todolist().having(tasks=[first_task])
    todolist_set.feed(todolist)

    task_key_generator.feed(expected_task.to_key())

    sut.execute(todolist_key=todolist.to_key(), task_key=expected_task.to_key(), name=expected_task.name)

    actual = todolist_set.by(todolist_key=todolist.to_key()).value
    assert actual == todolist.having(tasks=[first_task, expected_task]).to_snapshot()


def test_tell_ok_when_open_task(sut, todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest,
                                fake: TodolistFaker):
    # data
    todolist = fake.a_todolist()
    open_task = fake.a_task()

    # given
    todolist_set.feed(todolist)
    task_key_generator.feed(open_task.to_key())

    # when
    response = sut.execute(todolist_key=todolist.to_key(), task_key=open_task.to_key(), name=open_task.to_name())

    # then
    assert response == Ok(None)


def test_tell_error_when_open_task_for_unknown_todolist(sut: OpenTaskUseCase, todolist_set: TodolistSetForTest,
                                                        fake: TodolistFaker):
    # GIVEN
    unknown_todolist = fake.a_todolist()
    any_task = fake.a_task()
    todolist_set.feed_nothing(unknown_todolist.to_key())

    # WHEN
    response = sut.execute(todolist_key=unknown_todolist.to_key(), task_key=any_task.to_key(), name=any_task.to_name())

    # THEN
    assert response == Error("todolist not found")
