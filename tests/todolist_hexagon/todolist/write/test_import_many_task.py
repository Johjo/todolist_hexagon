import pytest
from expression import Ok, Error

from todolist_hexagon.todolist.write.import_many_task import ImportManyTask, ExternalTodoListPort, TaskImported
from todolist_hexagon.use_case_dependencies import UseCaseDependencies

from todolist_hexagon.builder import TodolistFaker, TaskBuilder
from tests.todolist_hexagon.todolist.fixture import TaskKeyGeneratorForTest, TodolistSetForTest
from tests.todolist_hexagon.adapter_dependencies_for_test import AdapterDependenciesForTest

@pytest.fixture
def task_key_generator() -> TaskKeyGeneratorForTest:
    return TaskKeyGeneratorForTest()


@pytest.fixture
def sut(todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest) -> ImportManyTask:
    return UseCaseDependencies(AdapterDependenciesForTest(todolist_set, task_key_generator)).import_many_task()


class ExternalTodolistForTest(ExternalTodoListPort):
    def __init__(self) -> None:
        self._tasks: list[TaskImported] | None = None

    def all_tasks(self) -> list[TaskImported]:
        if self._tasks is None:
            raise Exception("fed task before")
        return self._tasks

    def feed(self, *tasks: TaskImported):
        self._tasks = list(tasks)


@pytest.fixture
def external_todolist() -> ExternalTodolistForTest:
    return ExternalTodolistForTest()


def test_import_many_task(sut: ImportManyTask, todolist_set: TodolistSetForTest,
                          external_todolist: ExternalTodolistForTest, fake: TodolistFaker,
                          task_key_generator: TaskKeyGeneratorForTest):
    task_1 = fake.a_task(1)
    task_2 = fake.a_task(2).having(execution_date=fake.a_date())
    expected_tasks = [task_1, task_2]

    external_todolist.feed(*to_imported_task_list(expected_tasks))
    task_key_generator.feed(*[task for task in expected_tasks])
    todolist = fake.a_todolist()
    todolist_set.feed(todolist)

    sut.execute(todolist_key=todolist.to_key(), external_todolist=external_todolist)

    actual = todolist_set.by(todolist_key=todolist.to_key()).value
    assert actual == todolist.having(tasks=expected_tasks).to_snapshot()


def test_import_many_task_when_existing_task(sut: ImportManyTask, todolist_set: TodolistSetForTest,
                                             external_todolist: ExternalTodolistForTest, fake: TodolistFaker,
                                             task_key_generator: TaskKeyGeneratorForTest):
    first_task = fake.a_task(key=1)
    expected_task = fake.a_task(key=2)
    external_todolist.feed(to_imported_task(expected_task))
    task_key_generator.feed(expected_task)
    todolist = fake.a_todolist().having(tasks=[first_task])
    todolist_set.feed(todolist)

    sut.execute(todolist_key=todolist.to_key(), external_todolist=external_todolist)

    actual = todolist_set.by(todolist_key=todolist.to_key()).value
    assert actual == todolist.having(tasks=[first_task, expected_task]).to_snapshot()


def test_tell_ok_when_import_task(sut: ImportManyTask, todolist_set: TodolistSetForTest,
                                  external_todolist: ExternalTodolistForTest, fake: TodolistFaker,
                                  task_key_generator: TaskKeyGeneratorForTest):
    # GIVEN
    imported_tasks = [fake.a_task(), fake.a_task()]
    external_todolist.feed(*to_imported_task_list(imported_tasks))
    task_key_generator.feed(*imported_tasks)
    todolist = fake.a_todolist()
    todolist_set.feed(todolist)

    # WHEN
    response = sut.execute(todolist_key=todolist.to_key(), external_todolist=external_todolist)

    # THEN
    assert response == Ok(None)


def test_tell_error_when_todolist_doest_not_exist(sut: ImportManyTask, todolist_set: TodolistSetForTest,
                                                  external_todolist: ExternalTodolistForTest, fake: TodolistFaker):
    # GIVEN
    unknown_todolist = fake.a_todolist()
    todolist_set.feed_nothing(unknown_todolist.to_key())

    # WHEN
    response = sut.execute(unknown_todolist.to_key(), external_todolist)

    # THEN
    assert response == Error("todolist not found")


def to_imported_task_list(expected_tasks: list[TaskBuilder]) -> list[TaskImported]:
    return [to_imported_task(task) for task in expected_tasks]


def to_imported_task(task: TaskBuilder) -> TaskImported:
    return TaskImported(name=task.to_name(), is_open=task.to_open(), execution_date=task.to_execution_date())
