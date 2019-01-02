import re
import string
from collections import namedtuple
from typing import List, Dict, Tuple


class StepNode(object):

    def __init__(self, instruction: 'Instructions', name: str, duration: int=None) -> None:
        self.instructions = instruction
        self.name = name
        self.processed = 0
        self.previous: List[str] = []
        self.next: List[str] = []
        if duration is None:
            duration = 61 + string.ascii_uppercase.index(self.name)
        self.duration = duration

    def __eq__(self, other: 'StepNode') -> bool:
        return self.name == other.name

    def __ne__(self, other: 'StepNode') -> bool:
        return not self == other

    def __str__(self):
        return '%s (processed=%d/%d)' % (self.name, self.processed, self.duration)

    def __hash__(self):
        return hash(self.name)

    def completes_before(self, other: 'StepNode') -> None:
        if other.instructions != self.instructions:
            raise ValueError('Not in the same container')
        if other == self:
            raise ValueError('Same object')
        self.next.append(other.name)
        other.previous.append(self.name)

    def reset(self):
        self.processed = 0

    def get_next(self) -> 'List[StepNode]':
        return [self.instructions[n] for n in self.next]

    def process(self):
        self.processed += 1
        return self.processed >= self.duration

    @property
    def is_first(self) -> bool:
        return not self.previous

    @property
    def is_ready(self) -> bool:
        if self.previous:
            return all((self.instructions[prev].is_finished for prev in self.previous))
        return True

    @property
    def is_finished(self):
        return self.processed >= self.duration


ProcessResults = namedtuple('ProcessResults', ['order', 'duration', 'nops', 'workers'])


class Instructions(object):

    line_fmt = re.compile('^Step (?P<first>.) must be finished before step (?P<second>.) can begin.$')

    def __init__(self):
        self.nodes: Dict[str, StepNode] = {}

    def __getitem__(self, node_name: str) -> StepNode:
        return self.nodes[node_name]

    def add(self, node_name: str, duration: int=None) -> StepNode:
        node = self.nodes.get(node_name)
        if node is None:
            node = StepNode(self, node_name, duration)
            self.nodes[node_name] = node
        return node

    def _reset(self) -> None:
        for n in self.nodes.values():
            n.reset()

    @classmethod
    def from_file(cls, filename: str) -> 'Instructions':
        instructions = cls()

        with open(filename) as f:
            for l in f.readlines():
                fmt = cls.line_fmt.search(l)
                first = fmt.group('first')
                second = fmt.group('second')
                first_node = instructions.add(first)
                second_node = instructions.add(second)

                first_node.completes_before(second_node)

        print('Loaded %d nodes from %s' % (len(instructions.nodes), filename))
        return instructions

    def first_nodes(self) -> List[StepNode]:
        return sorted([
            n for n in self.nodes.values() if n.is_first
        ], key=lambda k: k.name)

    def _complete(self):
        return all([n.is_finished for n in self.nodes.values()])

    def process(self, n_workers: int=1) -> ProcessResults:
        if n_workers < 1:
            raise ValueError('Need at least 1 worker')

        order = []
        self._reset()

        current_nodes = self.first_nodes()
        processing = []

        duration = 0
        nops = 0  # no operations
        while not self._complete():

            while len(processing) < n_workers:
                # Add a new node to be processed
                # print('current_nodes=%s' % ','.join([n.name for n in current_nodes]))
                ready_nodes = [m for m in current_nodes if m.is_ready]
                # print('ready_nodes=%s' % ','.join([n.name for n in ready_nodes]))
                if not ready_nodes:
                    nops += (n_workers - len(processing))
                    break  # No nodes are ready
                node = ready_nodes[0]
                current_nodes.remove(node)

                for n in node.get_next():
                    if not n.is_finished and not n in current_nodes:
                        current_nodes.append(n)

                processing.append(node)

            new_processing = []
            for p in processing:
                if p.process():
                    order.append(p.name)
                else:
                    new_processing.append(p)
            processing = new_processing
            duration += 1

            # Ensure the queue is sorted alphabetically
            current_nodes = sorted(current_nodes, key=lambda k: k.name)

        return ProcessResults(order, duration, nops, n_workers)


if '__main__' == __name__:

    instructions = Instructions.from_file('input.txt')

    serial = instructions.process()
    print('Serial order is %s (duration %ds %d nops)' % (''.join(serial.order), serial.duration, serial.nops))

    n_workers = 5
    parallel = instructions.process(n_workers)
    print('Parallel order with %d workers is %s (duration %ds %d nops)' % (
        n_workers,
        ''.join(parallel.order),
        parallel.duration, parallel.nops
    ))
