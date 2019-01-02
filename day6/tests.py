import pytest

from day6.compute import Point, Map, Zone


@pytest.mark.parametrize('filename', ('test1.txt', 'test2.txt'))
def test_loading(filename):
    expected = [
        Point(1, 1),
        Point(8, 3),
        Point(3, 4),
        Point(5, 5),
        Point(1, 6),
        Point(8, 9),
    ]
    loaded = Map.from_file(filename)
    assert expected == loaded.pois, 'got %s' % ', '.join([str(c) for c in loaded.pois])
    assert 9 == loaded.height, 'got %d' % loaded.height
    assert 8 == loaded.width, 'got %d' % loaded.width


def test_distance():
    A = Point(1, 1)
    C = Point(8, 3)
    D = Point(3, 4)
    E = Point(5, 5)
    B = Point(1, 6)
    F = Point(8, 9)

    rv = A.distance(1, 1)
    assert 0 == rv, 'got %d' % rv
    rv = A.distance(0, 0)
    assert 2 == rv, 'got %d' % rv
    rv = C.distance(6, 1)
    assert 4 == rv, 'got %d' % rv
    rv = E.distance(6, 1)
    assert 5 == rv, 'got %d' % rv

    assert 2 == A.distance(0, 0)
    assert 11 == C.distance(0, 0)
    assert 7 == D.distance(0, 0)
    assert 10 == E.distance(0, 0)
    assert 7 == B.distance(0, 0)
    assert 17 == F.distance(0, 0)


def test_closeness():
    loaded = Map.from_file('test1.txt')
    assert loaded.closest_raster is None
    loaded._populate_rasters()
    assert loaded.closest_raster is not None

    def print_row(r):
        pr = []
        for e in r:
            pr.append('{' + ', '.join([str(p) for p in e]) + '}')
        return '[' + ', '.join(pr) + ']'

    A = Point(1, 1)
    C = Point(8, 3)
    D = Point(3, 4)
    E = Point(5, 5)
    B = Point(1, 6)
    F = Point(8, 9)

    assert [A] == loaded.closest(0, 0)[0]  # outside of raster but should not matter
    assert [C] == loaded.closest(9, 1)[0]

    assert 9 == len(loaded.closest_raster), 'got %d' % len(loaded.closest_raster)
    assert 8 == len(loaded.closest_raster[0]), 'got %d' % len(loaded.closest_raster[0])

    rows = [
        [ [A],    [A],    [A],       [A], [A, E], [C], [C], [C], ],  # 0
        [ [A],    [A],    [D],       [D], [E],    [C], [C], [C], ],
        [ [A],    [D],    [D],       [D], [E],    [C], [C], [C], ],
        [ [D, B], [D],    [D],       [D], [E],    [E], [C], [C], ],  # 3
        [ [B],    [D, B], [D],       [E], [E],    [E], [E], [C], ],
        [ [B],    [B],    [D, B],    [E], [E],    [E], [E], [C, F], ],
        [ [B],    [B],    [D, B],    [E], [E],    [E], [F], [F], ],  # 6
        [ [B],    [B],    [D, B],    [E], [E],    [F], [F], [F], ],
        [ [B],    [B],    [D, B, F], [F], [F],    [F], [F], [F], ],
        # 9
    ]
    for i, row in enumerate(loaded.closest_raster):
        assert rows[i] == row, '%s vs\n row=%d y=%d row=%s' % (
            print_row(rows[i]),
            i,
            loaded.first_point.y + i,
            print_row(row),
        )


def test_zone():

    def print_zones(zones):
        return ', '.join([
            str(p.point) + '{%d}' % (p.area if p.area is not None else -1)
            for p in zones
        ])

    loaded = Map.from_file('test1.txt')
    expected = [
        Zone(Point(5, 5), 17),
        Zone(Point(3, 4), 9),
        Zone(Point(1, 1), None),
        Zone(Point(8, 3), None),
        Zone(Point(1, 6), None),
        Zone(Point(8, 9), None),
    ]
    rv = loaded.danger_zones()
    assert expected == rv, 'got %s expected\n  %s' % (print_zones(rv), print_zones(expected))


def test_common_zone():

    loaded = Map.from_file('test1.txt')
    expected = [
        Point(3, 3),
        Point(4, 3),
        Point(5, 3),
        Point(2, 4),
        Point(3, 4),
        Point(4, 4),
        Point(5, 4),
        Point(6, 4),
        Point(2, 5),
        Point(3, 5),
        Point(4, 5),
        Point(5, 5),
        Point(6, 5),
        Point(3, 6),
        Point(4, 6),
        Point(5, 6),
    ]
    zone = loaded.common_zone(32)

    rv = loaded.closest(0, 0)
    assert 10 + 7 + 2 + 11 + 7 + 17 == rv[1], 'got %d' % rv[1]  # outside of raster but should not matter
    rv = loaded.closest(9, 1)
    assert 8 + 3 + 9 + 8 + 13 + 9 == rv[1], 'got %d' % rv[1]
    rv = loaded.closest(4, 3)
    assert 5 + 4 + 2 + 3 + 6 + 10 == rv[1], 'got %d' % rv[1]

    assert expected == zone, 'got %s' % ', '.join([str(p) for p in zone])
