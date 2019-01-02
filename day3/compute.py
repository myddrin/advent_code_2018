"""
Answer to https://adventofcode.com/2018/day/3
"""
import re
from collections import namedtuple
from typing import List


Position = namedtuple('Position', ['x', 'y'])


class Rect(object):

    def __init__(self, id: int, left: int, top: int, width: int, height: int):
        self.id = id
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    @property
    def right(self):
        return self.left + self.width

    @property
    def bottom(self):
        return self.top + self.height

    @property
    def surface(self):
        return self.width * self.height

    def positions(self):
        rv = []
        for y in range(self.top, self.bottom):
            for x in range(self.left, self.right):
                rv.append(Position(x, y))
        return rv

    def __str__(self):
        return 'Rect(%d,%d %dx%d)' % (self.left, self.top, self.width, self.height)


class Raster(object):

    def __init__(self, shapes: List[Rect], width: int, height: int):
        print('Creating raster of %dx%d' % (width, height))
        self.surface = None
        self.width = width
        self.height = height

        self.shapes = shapes
        self._populate(shapes)

    def _populate(self, shapes: List[Rect]):
        self.surface = []
        for h in range(self.height):
            self.surface.append(list())
            for w in range(self.width):
                self.surface[h].append(list())
        for s in shapes:
            for pos in s.positions():
                if self.surface[pos.y][pos.x] is None:
                    self.surface[pos.y][pos.x] = [s.id]
                else:
                    self.surface[pos.y][pos.x].append(s.id)

    def overlapping_surface(self):
        surface = 0
        for line in self.surface:
            for col in line:
                if len(col) > 1:
                    surface += 1
        return surface

    def not_overlapping(self):
        assert self.surface is not None
        ids = {shape.id for shape in self.shapes}
        for line in self.surface:
            for col in line:
                if len(col) > 1:
                    for id in col:
                        if id in ids:
                            ids.remove(id)
        return list(ids)

    @classmethod
    def from_file(cls, filename: str):
        print('Loading from %s' % filename)
        fmt = re.compile('#([0-9]*) @ ([0-9]*),([0-9]*): ([0-9]*)x([0-9]*)$')
        shapes = []
        raster_width = 0
        raster_height = 0
        with open(filename) as f:
            for l in f.readlines():
                ptrn = fmt.search(l)
                shapes.append(Rect(
                    id=int(ptrn.group(1)),
                    left=int(ptrn.group(2)),
                    top=int(ptrn.group(3)),
                    width=int(ptrn.group(4)),
                    height=int(ptrn.group(5)),
                ))
                raster_width = max(raster_width, shapes[-1].right)
                raster_height = max(raster_height, shapes[-1].bottom)
        return cls(shapes, raster_width, raster_height)


if '__main__' == __name__:
    raster = Raster.from_file('input.txt')
    overlap = raster.overlapping_surface()  # 101469
    not_overlap = raster.not_overlapping()  # 1067

    print('overlap=%d (square inches)' % overlap)
    print('not overlapping %s' % ', '.join((str(id) for id in not_overlap)))
