from collections import OrderedDict

import pytest

from src.todolist_hexagon.fvp.aggregate import Task, NothingToDo, DoTheTask, ChooseTheTask, FinalVersionPerfectedSession, \
    FvpSnapshot
from tests.fixture import a_task_key


@pytest.fixture
def sut():
    return FinalVersionPerfectedSession.create()


def test_propose_nothing_when_empty(sut):
    actual = sut.which_task([])
    assert actual == NothingToDo()


def test_when_one_task_propose_the_only_task_open_when_one(sut):
    task = Task(key=1)

    actual = sut.which_task([task])
    assert actual == DoTheTask(key=task.key)


def test_when_two_tasks_propose_to_choose_both(sut):
    open_task = [Task(key=a_task_key(1)), Task(key=a_task_key(2))]

    actual = sut.which_task(open_task)
    assert actual == ChooseTheTask(main_task_key=a_task_key(1), secondary_task_key=a_task_key(2))


@pytest.mark.parametrize("chosen_task,ignored_task,expected", [
    (1, 2, DoTheTask(key=a_task_key(1))),
    (2, 1, DoTheTask(key=a_task_key(2))),

])
def test_when_two_tasks_propose_to_do_chosen_task(sut, chosen_task, ignored_task, expected):
    sut.choose_and_ignore_task(id_chosen=a_task_key(chosen_task), id_ignored=a_task_key(ignored_task))

    open_tasks = [Task(key=a_task_key(1)), Task(key=a_task_key(2))]
    actual = sut.which_task(open_tasks)
    assert actual == expected


def test_when_two_tasks_reopen_deffered_task_when_previous_task_is_done(sut):
    open_tasks = [Task(key=a_task_key(1)), Task(key=a_task_key(2))]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(1), secondary_task_key=a_task_key(2))

    sut.choose_and_ignore_task(a_task_key(1), a_task_key(2))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(1))

    open_tasks.remove(Task(key=a_task_key(1)))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(2))


def test_when_two_propose_first_task_when_last_is_closed(sut):
    open_tasks = [Task(key=a_task_key(1)), Task(key=a_task_key(2))]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(1), secondary_task_key=a_task_key(2))

    sut.choose_and_ignore_task(a_task_key(2), a_task_key(1))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(2))

    open_tasks.remove(Task(key=a_task_key(2)))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(1))


def test_when_three_evaluate_from_previous_chosen_task_when_close_one(sut):
    open_tasks = [Task(key=a_task_key(1)), Task(key=a_task_key(2)),
                  Task(key=a_task_key(3))]

    sut.choose_and_ignore_task(a_task_key(1), a_task_key(2))
    sut.choose_and_ignore_task(a_task_key(3), a_task_key(1))

    open_tasks.remove(Task(key=a_task_key(3)))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(1))


def test_when_four_propose_tasks_in_good_order_after_close_one(sut):
    open_tasks = [Task(key=a_task_key(1)), Task(key=a_task_key(2)),
                  Task(key=a_task_key(3)), Task(key=a_task_key(4))]

    sut.choose_and_ignore_task(a_task_key(2), a_task_key(1))
    sut.choose_and_ignore_task(a_task_key(3), a_task_key(2))
    sut.choose_and_ignore_task(a_task_key(3), a_task_key(4))
    open_tasks.remove(Task(key=a_task_key(3)))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(2), secondary_task_key=a_task_key(4))


### -----
def test_acceptance_with_no_tasks(sut):
    actual = sut.which_task([])
    assert actual == NothingToDo()


def test_acceptance_with_one_tasks(sut):
    open_tasks = [Task(key=a_task_key(1))]
    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(1))


def test_acceptance_with_two_tasks_01(sut):
    open_tasks = [Task(key=a_task_key(1)), Task(key=a_task_key(2))]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(1), secondary_task_key=a_task_key(2))

    sut.choose_and_ignore_task(a_task_key(1), a_task_key(2))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(1))

    open_tasks.remove(Task(key=a_task_key(1)))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(2))

    open_tasks.remove(Task(key=a_task_key(2)))

    actual = sut.which_task(open_tasks)
    assert actual == NothingToDo()


def test_acceptance_with_two_tasks_02(sut):
    open_tasks = [Task(key=a_task_key(1)), Task(key=a_task_key(2))]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(1), secondary_task_key=a_task_key(2))

    sut.choose_and_ignore_task(a_task_key(2), a_task_key(1))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(2))

    open_tasks.remove(Task(key=a_task_key(2)))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(1))

    open_tasks.remove(Task(key=a_task_key(1)))

    actual = sut.which_task(open_tasks)
    assert actual == NothingToDo()


def test_acceptance_with_three_tasks_01(sut):
    open_tasks = [Task(key=a_task_key(1)), Task(key=a_task_key(2)),
                  Task(key=a_task_key(3))]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(1), secondary_task_key=a_task_key(2))

    sut.choose_and_ignore_task(a_task_key(1), a_task_key(2))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(1), secondary_task_key=a_task_key(3))

    sut.choose_and_ignore_task(a_task_key(1), a_task_key(3))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(1))

    open_tasks.remove(Task(key=a_task_key(1)))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(2), secondary_task_key=a_task_key(3))

    sut.choose_and_ignore_task(a_task_key(2), a_task_key(3))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(2))

    open_tasks.remove(Task(key=a_task_key(2)))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(3))

    open_tasks.remove(Task(key=a_task_key(3)))

    actual = sut.which_task(open_tasks)
    assert actual == NothingToDo()


def test_acceptance_with_three_tasks_02(sut):
    open_tasks = [Task(key=a_task_key(1)), Task(key=a_task_key(2)),
                  Task(key=a_task_key(3))]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(1), secondary_task_key=a_task_key(2))

    sut.choose_and_ignore_task(a_task_key(1), a_task_key(2))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(1), secondary_task_key=a_task_key(3))

    sut.choose_and_ignore_task(a_task_key(3), a_task_key(1))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(3))

    open_tasks.remove(Task(key=a_task_key(3)))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(1))

    open_tasks.remove(Task(key=a_task_key(1)))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(2))

    open_tasks.remove(Task(key=a_task_key(2)))

    actual = sut.which_task(open_tasks)
    assert actual == NothingToDo()


def test_acceptance_with_three_tasks_03(sut):
    open_tasks = [Task(key=a_task_key(1)), Task(key=a_task_key(2)),
                  Task(key=a_task_key(3))]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(1), secondary_task_key=a_task_key(2))

    sut.choose_and_ignore_task(a_task_key(2), a_task_key(1))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(2), secondary_task_key=a_task_key(3))

    sut.choose_and_ignore_task(a_task_key(3), a_task_key(2))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(3))

    open_tasks.remove(Task(key=a_task_key(3)))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(2))

    open_tasks.remove(Task(key=a_task_key(2)))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(1))

    open_tasks.remove(Task(key=a_task_key(1)))

    actual = sut.which_task(open_tasks)
    assert actual == NothingToDo()


def test_acceptance_with_four_tasks_01(sut):
    open_tasks = [Task(key=a_task_key(1)), Task(key=a_task_key(2)),
                  Task(key=a_task_key(3)), Task(key=a_task_key(4))]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(1), secondary_task_key=a_task_key(2))

    sut.choose_and_ignore_task(a_task_key(2), a_task_key(1))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(2), secondary_task_key=a_task_key(3))

    sut.choose_and_ignore_task(a_task_key(3), a_task_key(2))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(3), secondary_task_key=a_task_key(4))

    sut.choose_and_ignore_task(a_task_key(3), a_task_key(4))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(3))  # here

    open_tasks.remove(Task(key=a_task_key(3)))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(2), secondary_task_key=a_task_key(4))

    sut.choose_and_ignore_task(a_task_key(2), a_task_key(4))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(2))

    open_tasks.remove(Task(key=a_task_key(2)))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(1), secondary_task_key=a_task_key(4))

    sut.choose_and_ignore_task(a_task_key(4), a_task_key(1))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(4))

    open_tasks.remove(Task(key=a_task_key(4)))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(1))

    open_tasks.remove(Task(key=a_task_key(1)))

    actual = sut.which_task(open_tasks)
    assert actual == NothingToDo()


# - [ ] Email  #testfvp
# - [ ] In-Tray #testfvp
# - [ ] (3) Voicemail #testfvp
# - [ ] Project X Report #testfvp
# - [ ] (1) Tidy Desk #testfvp
# - [ ] Call Dissatisfied Customer #testfvp
# - [ ] (4) Make Dental Appointment #testfvp
# - [ ] File Invoices #testfvp
# - [ ] Discuss Project Y with Bob #testfvp
# - [ ] (2)Back Up   #testfvp


def test_acceptance_full(sut):
    open_tasks = [Task(key=a_task_key(1)), Task(key=a_task_key(2)),
                  Task(key=a_task_key(3)), Task(key=a_task_key(4)),
                  Task(key=a_task_key(5)), Task(key=a_task_key(6)),
                  Task(key=a_task_key(7)), Task(key=a_task_key(8)),
                  Task(key=a_task_key(9)), Task(key=a_task_key(10))]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(1), secondary_task_key=a_task_key(2))

    sut.choose_and_ignore_task(a_task_key(1), a_task_key(2))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(1), secondary_task_key=a_task_key(3))

    sut.choose_and_ignore_task(a_task_key(3), a_task_key(1))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(3), secondary_task_key=a_task_key(4))

    sut.choose_and_ignore_task(a_task_key(3), a_task_key(4))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(3), secondary_task_key=a_task_key(5))

    sut.choose_and_ignore_task(a_task_key(5), a_task_key(3))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(5), secondary_task_key=a_task_key(6))

    sut.choose_and_ignore_task(a_task_key(5), a_task_key(6))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(5), secondary_task_key=a_task_key(7))

    sut.choose_and_ignore_task(a_task_key(5), a_task_key(7))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(5), secondary_task_key=a_task_key(8))

    sut.choose_and_ignore_task(a_task_key(5), a_task_key(8))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(5), secondary_task_key=a_task_key(9))

    sut.choose_and_ignore_task(a_task_key(5), a_task_key(9))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(5), secondary_task_key=a_task_key(10))

    sut.choose_and_ignore_task(a_task_key(5), a_task_key(10))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(5))

    open_tasks.remove(Task(key=a_task_key(5)))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(3), secondary_task_key=a_task_key(6))

    sut.choose_and_ignore_task(a_task_key(3), a_task_key(6))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(3), secondary_task_key=a_task_key(7))

    sut.choose_and_ignore_task(a_task_key(7), a_task_key(3))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(7), secondary_task_key=a_task_key(8))

    sut.choose_and_ignore_task(a_task_key(7), a_task_key(8))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(7), secondary_task_key=a_task_key(9))

    sut.choose_and_ignore_task(a_task_key(7), a_task_key(9))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(main_task_key=a_task_key(7), secondary_task_key=a_task_key(10))

    sut.choose_and_ignore_task(a_task_key(10), a_task_key(7))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(key=a_task_key(10))

    open_tasks.remove(Task(key=a_task_key(10)))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(a_task_key(7))





def test_empty_snapshot(sut):
    snapshot = sut.to_snapshot()
    assert snapshot == FvpSnapshot(OrderedDict())

def test_write_priorities_to_snapshot(sut):
    sut.choose_and_ignore_task(a_task_key(1), a_task_key(2))
    snapshot = sut.to_snapshot()
    assert snapshot == FvpSnapshot(OrderedDict({a_task_key(2): a_task_key(1)}))

def test_read_priorities_from_snapshot(sut):
    snapshot = FvpSnapshot(OrderedDict({a_task_key(1): 1, a_task_key(2): 0}))
    sut = FinalVersionPerfectedSession.from_snapshot(snapshot)
    assert sut.to_snapshot() == FvpSnapshot(OrderedDict({a_task_key(1): 1, a_task_key(2): 0}))

def test_reset_session(sut):
    sut.choose_and_ignore_task(a_task_key(1), a_task_key(2))
    sut.reset()
    assert sut.to_snapshot() == FvpSnapshot(OrderedDict())
