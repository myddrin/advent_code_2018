from day03.compute import Raster, Rect, Position


def test_loading():
    raster = Raster.from_file('test1.txt')
    expected = [
        Rect(1, 1, 3, 4, 4),
        Rect(2, 3, 1, 4, 4),
        Rect(3, 5, 5, 2, 2),
    ]
    assert 7 == raster.width, 'width=%d' % raster.width
    assert 7 == raster.height, 'height=%d' % raster.height
    shapes = raster.shapes
    for i, s in enumerate(expected):
        assert s.id == shapes[i].id, 'id %s vs %s' % (str(s), str(shapes[i]))
        assert s.left == shapes[i].left, 'left %s vs %s' % (str(s), str(shapes[i]))
        assert s.top == shapes[i].top, 'top %s vs %s' % (str(s), str(shapes[i]))
        assert s.width == shapes[i].width, 'width %s vs %s' % (str(s), str(shapes[i]))
        assert s.height == shapes[i].height, 'height %s vs %s' % (str(s), str(shapes[i]))


def test_positions():
    rec = Rect(1, 1, 3, 4, 4)
    assert [
        Position(1, 3), Position(2, 3), Position(3, 3), Position(4, 3),
        Position(1, 4), Position(2, 4), Position(3, 4), Position(4, 4),
        Position(1, 5), Position(2, 5), Position(3, 5), Position(4, 5),
        Position(1, 6), Position(2, 6), Position(3, 6), Position(4, 6),
    ] == rec.positions()


def test_overloap():
    raster = Raster.from_file('test1.txt')
    overlap = raster.overlapping_surface()
    assert 4 == overlap, 'overlap=%d' % overlap


def test_not_overlapping():
    raster = Raster.from_file('test1.txt')
    not_overlap = raster.not_overlapping()
    assert [3] == not_overlap, 'not_overlap=%r' % not_overlap
