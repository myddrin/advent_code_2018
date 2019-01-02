"""
Answer to https://adventofcode.com/2018/day/4
"""
import re
from datetime import date, datetime, timedelta
from enum import IntEnum
from typing import Dict, List


Status = IntEnum('Status', ['Begin', 'Awake', 'Asleep'])


class GuardState(object):

    time_fmt = '%Y-%m-%d %H:%M'
    line_fmt = re.compile( '\[(.*)\] ([\w]*) (.*)$')

    def __init__(self, when: datetime, id: int, status: Status):
        self.id = id
        self.when = when
        self.status = status

    def __str__(self):
        return '[%s] #%r %s' % (self.when.strftime(self.time_fmt), self.id, self.status.name)

    def __eq__(self, other):
        return self.id == other.id and self.when == other.when and self.status == other.status

    def __ne__(self, other):
        return not self == other

    @property
    def is_awake(self):
        return self.status in [Status.Begin, Status.Awake]

    @property
    def is_asleep(self):
        return Status.Asleep == self.status

    @classmethod
    def from_str(cls, string):  # -> GuardState
        fmt = cls.line_fmt.search(string)
        if fmt is None:
            raise ValueError('Incorrectly formatted string: %r' % string)
        when = datetime.strptime(fmt.group(1), cls.time_fmt)
        action = fmt.group(2)
        leftover = fmt.group(3)
        id = None
        if action.lower() == 'guard':
            id = int(leftover.split(' ')[0].replace('#', ''))
            status = Status.Begin
        elif action.lower() == 'wakes':
            status = Status.Awake
        elif action.lower() == 'falls':
            status = Status.Asleep
        else:
            raise ValueError('Unexpected action %s' % action)
        return cls(when, id, status)


class GuardInfo(object):

    class MinDetails(object):

        def __init__(self, minute: int, values: List[date]):
            self.minute = minute
            self.values = values

        def __str__(self):
            return '%d->[%s](%d)' % (
                self.minute,
                ', '.join([d.strftime('%Y-%m-%d') for d in self.values]),
                len(self.values)
            )

        @property
        def length(self):
            return len(self.values)

    def __init__(self, data: List=None, asleep: int=0, by_minutes: List=None):
        self.id = data[0].id if data else None
        self.data = data
        self.asleep = asleep
        self.by_minutes = by_minutes if by_minutes is not None else list()

    @property
    def worst_minute(self):
        if self.by_minutes:
            return self.by_minutes[0].minute
        return None

    @property
    def worst_length(self):
        if self.by_minutes:
            return self.by_minutes[0].length
        print('W: No data for %s' % str(self))
        return 0

    def __str__(self):
        return '#%r asleep=%d by_minutes=[%s]' % (
            self.id,
            self.asleep,
            ', '.join([str(d) for d in self.by_minutes])
        )


class Schedule(object):

    def __init__(self, filename):

        data = []
        print('Loading from %s' % filename)
        with open(filename) as f:
            for l in f.readlines():
                data.append(GuardState.from_str(l.rstrip()))

        self.data = sorted(data, key=lambda a: a.when)
        self._by_guard = None
        if not data:
            raise ValueError('No data')
        if self.data[0].id is None:
            raise ValueError('First entry %s does not have an ID' % str(self.data[0]))
        last_id = self.data[0].id
        for d in self.data[1:]:
            if d.id is None:
                d.id = last_id
            else:
                last_id = d.id
        print('Sorted %d entries between %s and %s' % (
            len(self.data),
            self.data[0].when.strftime(GuardState.time_fmt),
            self.data[-1].when.strftime(GuardState.time_fmt),
        ))

    def __str__(self):
        return '\n'.join([str(d) for d in self.data])

    def _populate_by_guard(self):  # -> None
        if self._by_guard is not None:
            return

        by_guard: Dict[int, GuardInfo] = {}
        for d in self.data:
            if d.id in by_guard:
                by_guard[d.id].data.append(d)
            else:
                by_guard[d.id] = GuardInfo([d])

        for g in by_guard.values():
            previous = g.data[0]
            total_asleep = 0
            minutes_asleep: Dict[int, List[date]] = {}
            assert previous.is_awake, 'Assuming a guard starts duty awake, got %s' % str(previous)
            for d in g.data[1:]:
                time_diff = d.when - previous.when
                if previous.is_asleep:
                    if time_diff.seconds < 23 * 3600:
                        # If the time delta is 23h the last info is not from today's shift
                        total_asleep += time_diff.seconds // 60
                        curr_time = previous.when
                        while curr_time < d.when:
                            if 0 == curr_time.hour:
                                minute = curr_time.minute
                                if minute in minutes_asleep:
                                    minutes_asleep[minute].append(curr_time.date())
                                else:
                                    minutes_asleep[minute] = [curr_time.date()]
                            curr_time += timedelta(minutes=1)
                    else:
                        assert False, 'Unexpected guard still asleep at the end of the shift %s (diff=%s prev=%s)' % (
                            str(d),
                            str(time_diff),
                            str(previous),
                        )
                previous = d

            g.asleep = total_asleep
            g.by_minutes = sorted([
                GuardInfo.MinDetails(k, v)
                for k, v in minutes_asleep.items()
            ], key=lambda v: v.length, reverse=True)

        self._by_guard = by_guard.values()

    def by_guard(self, sort_by_total=True):
        self._populate_by_guard()
        if sort_by_total:
            return sorted(self._by_guard, key=lambda v: v.asleep, reverse=True)
        return sorted(self._by_guard, key=lambda v: v.worst_length, reverse=True)


if '__main__' == __name__:

    rotations = Schedule('input.txt')

    by_total = rotations.by_guard()[0]

    print('Most asleep guard is #%d with %d minutes' % (by_total.id, by_total.asleep))
    print('This guard is most often asleep during minute %d' % (by_total.worst_minute))
    print('answer=%d' % (by_total.id * by_total.worst_minute))  # 95199

    by_minute = rotations.by_guard(sort_by_total=False)[0]

    print('The guard most regularily asleep is #%d on minute %d' % (by_minute.id, by_minute.worst_minute))
    print('answer=%d' % (by_minute.id * by_minute.worst_minute))  # 7887
