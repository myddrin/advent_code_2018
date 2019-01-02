import pytest

from day07.compute import Instructions, StepNode


@pytest.fixture
def expected_test1() -> Instructions:
    instructions = Instructions()
    A = instructions.add('A', 1)
    B = instructions.add('B', 2)
    C = instructions.add('C', 3)
    D = instructions.add('D', 4)
    E = instructions.add('E', 5)
    F = instructions.add('F', 6)

    C.completes_before(A)
    C.completes_before(F)
    A.completes_before(B)
    A.completes_before(D)
    B.completes_before(E)
    D.completes_before(E)
    F.completes_before(E)

    return instructions


def test_loading(expected_test1):
    instructions = Instructions.from_file('test1.txt')

    assert sorted([n.name for n in expected_test1.nodes.values()]) == sorted([n.name for n in instructions.nodes.values()])

    for node in expected_test1.nodes.values():
        assert sorted(node.previous) == sorted(instructions[node.name].previous)
        assert sorted(node.next) == sorted(instructions[node.name].next)
        assert 60 + node.duration == instructions[node.name].duration


def test_is_first(expected_test1):
    for n in expected_test1.nodes.values():
        if n.name == 'C':
            assert n.is_first, str(n)
        else:
            assert not n.is_first, str(n)


def test_is_ready(expected_test1):
    processed = []
    for idx, are_ready in enumerate(['C', 'AF', 'BDF', 'DF', 'F', 'E']):

        for n in expected_test1.nodes.values():
            if n.name in processed:
                assert n.is_finished, '%s idx=%d are_ready=%s' % (str(n), idx, are_ready)
                assert n.is_ready, '%s idx=%d are_ready=%s' % (str(n), idx, are_ready)
                continue

            assert not n.is_finished, '%s idx=%d are_ready=%s' % (str(n), idx, are_ready)

            if n.name in are_ready:
                assert n.is_ready, '%s idx=%d are_ready=%s' % (str(n), idx, are_ready)
            else:
                assert not n.is_ready, '%s idx=%d are_ready=%s' % (str(n), idx, are_ready)

        name = are_ready[0]
        processed.append(name)
        expected_test1[name].processed = expected_test1[name].duration


def test_first_nodes(expected_test1):

    for n in expected_test1.nodes.values():
        if n.name == 'C':
            assert n.is_first, str(n)
        else:
            assert not n.is_first, str(n)

    found = expected_test1.first_nodes()
    assert ['C'] == [n.name for n in found]

    first = expected_test1.add('1', 1)
    other_first = expected_test1.add('0', 1)
    first.completes_before(expected_test1['C'])
    other_first.completes_before(expected_test1['C'])

    found = expected_test1.first_nodes()
    assert ['0', '1'] == [n.name for n in found]


def test_serial_processing(expected_test1):
    rv = expected_test1.process()
    assert 'CABDFE' == ''.join(rv.order)
    assert 21 == rv.duration
    assert 0 == rv.nops


def test_parallel_processing(expected_test1):
    rv = expected_test1.process(2)
    assert 'CABFDE' == ''.join(rv.order)
    assert 15 == rv.duration
    assert 9 == rv.nops
