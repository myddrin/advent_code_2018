from datetime import datetime

import pytest

from day4.compute import Schedule, GuardState, Status


@pytest.mark.parametrize('filename', ('test1.txt', 'test1_unordered.txt'))
def test_loading(filename: str):
    rotations = Schedule(filename)
    expected = [
        GuardState(datetime(1518, 11, 1,  0,  0), 10, Status.Begin),
        GuardState(datetime(1518, 11, 1,  0,  5), 10, Status.Asleep),
        GuardState(datetime(1518, 11, 1,  0, 25), 10, Status.Awake),
        GuardState(datetime(1518, 11, 1,  0, 30), 10, Status.Asleep),
        GuardState(datetime(1518, 11, 1,  0, 55), 10, Status.Awake),
        GuardState(datetime(1518, 11, 1, 23, 58), 99, Status.Begin),
        GuardState(datetime(1518, 11, 2,  0, 40), 99, Status.Asleep),
        GuardState(datetime(1518, 11, 2,  0, 50), 99, Status.Awake),
        GuardState(datetime(1518, 11, 3,  0,  5), 10, Status.Begin),
        GuardState(datetime(1518, 11, 3,  0, 24), 10, Status.Asleep),
        GuardState(datetime(1518, 11, 3,  0, 29), 10, Status.Awake),
        GuardState(datetime(1518, 11, 4,  0,  2), 99, Status.Begin),
        GuardState(datetime(1518, 11, 4,  0, 36), 99, Status.Asleep),
        GuardState(datetime(1518, 11, 4,  0, 46), 99, Status.Awake),
        GuardState(datetime(1518, 11, 5,  0,  3), 99, Status.Begin),
        GuardState(datetime(1518, 11, 5,  0, 45), 99, Status.Asleep),
        GuardState(datetime(1518, 11, 5,  0, 55), 99, Status.Awake),
    ]
    for i, e in enumerate(expected):
        assert e == rotations.data[i], '%s == %s' % (str(e), str(rotations.data[i]))
    print('Done')


def test_by_guard():
    exp_10_total = 20 + 25 + 5
    exp_10_top = 24
    exp_99_total = 10 + 10 + 10
    exp_99_top = 45
    rotations = Schedule('test1.txt')

    by_total = rotations.by_guard()
    # print('by_total=%s'  '\n'.join([str(g) for g in by_total]))

    guard = by_total[0]
    assert 10 == guard.id, 'guard=%s' % str(guard)
    assert exp_10_total == guard.asleep, '%r != %r' % (exp_10_total, guard.asleep)
    assert exp_10_top == guard.worst_minute

    guard = by_total[1]
    assert 99 == guard.id, 'guard=%s' % str(guard)
    assert exp_99_total == guard.asleep, '%r != %r' % (exp_99_total, guard.asleep)
    assert exp_99_top == guard.worst_minute
    print('Done')

    by_minute = rotations.by_guard(sort_by_total=False)

    guard = by_minute[0]
    assert 99 == guard.id, 'guard=%s' % str(guard)

    guard = by_minute[1]
    assert 10 == guard.id, 'guard=%s' % str(guard)
