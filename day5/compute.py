"""
Answer to https://adventofcode.com/2018/day/%
"""
import re
import string

from collections import namedtuple


def is_reacting(unitA: str, unitB: str):  # -> bool
    return unitA.lower() == unitB.lower() and unitA.islower() != unitB.islower()


ReactionInfo = namedtuple('ReactionInfo', ['polymere', 'reactions', 'removed'])


def reaction(polymere: str):  # -> str
    assert len(polymere) > 1
    rv = polymere
    curr = 1
    n_reaction = 0

    print('Compressing polymere of %d units' % len(polymere))

    while curr < len(rv):
        prev = curr - 1
        # prev < 0 may happen when a lot of collapsing occurs

        if prev >= 0 and is_reacting(rv[prev], rv[curr]):
            old = rv
            try:
                rv = old[:prev] + old[curr + 1:]
            except MemoryError:
                print('at location prev=%d curr=%d' % (prev, curr))
                raise
            curr -= 2  # re-evaluate the previous step
            n_reaction += 1

        # if (curr + n_reaction) % 10000 == 9999:
            # print('Current polymere is %d units long after %d reactions (curr=%d)' % (len(rv), n_reaction, curr))

        curr += 1

    return ReactionInfo(rv, n_reaction, None)


def simplification(polymere: str, unit: str):
    rv = re.sub('[%s%s]' % (unit.lower(), unit.upper()), '', polymere)
    print('Simplified polymere is %d units long after removing unit %s' % (len(rv), unit))
    return rv


def best_simplification(polymere: str):  # -> Tuple[str, str]
    best_reacted = ReactionInfo(polymere, 0, None)  # not an actual reaction

    for unit in string.ascii_lowercase:
        simplified = simplification(polymere, unit)
        reacted = reaction(simplified)

        if len(reacted.polymere) < len(best_reacted.polymere):
            best_reacted = ReactionInfo(reacted.polymere, reacted.reactions, unit)
            print('New best polymere of %d units when removing %s' % (len(best_reacted.polymere), unit))

    return best_reacted


if '__main__' == __name__:

    with open('input.txt') as f:
        polymere = ''.join(f.readlines()).rstrip()

    assert 50000 == len(polymere), 'got %d' % len(polymere)
    rv = reaction(polymere)  # 11720

    print('Original polymere is %d units long after %d reactions' % (len(rv.polymere), rv.reactions))

    rv = best_simplification(polymere)  # 4956

    print('Best reduction is %d units long after %d reactions when removing units %s' % (
        len(rv.polymere),
        rv.reactions,
        rv.removed
    ))
