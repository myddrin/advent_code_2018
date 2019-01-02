"""
Answer to https://adventofcode.com/2018/day/6
"""
from typing import List

from collections import namedtuple


class Point(object):

    def __init__(self, x: int, y: int, map=None):
        self.x = x
        self.y = y
        self.map = map

    def __str__(self):
        return '(%d, %d)' % (self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        if self.map is None:
            raise ValueError('Cannot compute raster position without a map')
        return (self.y - self.map.first_point.y) * self.map.width + (self.x - self.map.first_point.x)

    def distance(self, x: int, y: int):
        """Manhattan distance"""
        return abs(x - self.x) + abs(y - self.y)


Zone = namedtuple('Zone', ['point', 'area'])


class Map(object):

    def __init__(self, pois: List[Point], first_point: Point, width: int, height: int):
        self.pois = []
        self.width = width
        self.height = height
        self.closest_raster = None
        self.distance_raster = None

        def raster_sort(p: Point):
            # Not using property because we cannot really do it yet
            return (p.y - first_point.y) * width + (p.x - first_point.x)

        self.pois = sorted([Point(p.x, p.y, self) for p in pois], key=raster_sort)


    def _populate_rasters(self):
        if self.closest_raster is not None and self.distance_raster is not None:
            return
        closest_raster = []  # 2D raster of List[Point] (closest)
        distance_raster = []  # 2D raster of int (sum of all distances)

        assert self.first_point.x >= 0
        assert self.first_point.y >= 0

        for y in range(self.height):
            closest_row = []
            distance_row = []
            for x in range(self.width):
                rv, total = self.closest(x + self.first_point.x, y + self.first_point.y)
                closest_row.append(rv)
                distance_row.append(total)

            closest_raster.append(closest_row)
            distance_raster.append(distance_row)

        self.closest_raster = closest_raster
        self.distance_raster = distance_raster

    def closest(self, x: int, y: int):  # -> Tuple[List[Point], int]
        closest_d = self.first_point.distance(x, y)
        closest = [self.first_point]
        total_distances = closest_d

        for p in self.pois[1:]:

            # if x == p.x and y == p.y:
                # return [p]  # It's on the point

            c = p.distance(x, y)
            total_distances += c
            if c < closest_d:
                closest = [p]
                closest_d = c
            elif c == closest_d:
                closest.append(p)

        return closest, total_distances

    def danger_zones(self):
        self._populate_rasters()

        # Find all zones on the corner of the raster and add them to the ignore list
        ignore_poi = set()
        for y, line in enumerate(self.closest_raster):
            if y == 0 or y == len(self.closest_raster):
                for points in line:
                    if len(points) != 1:
                        # Ignore ties for infinite
                        continue
                    ignore_poi.add(points[0])
            else:
                if len(line[0]) == 1:
                    ignore_poi.add(line[0][0])
                if len(line[-1]) == 1:
                    ignore_poi.add(line[-1][0])

        print('Ignoring infinite areas from points %s' % ', '.join([str(p) for p in ignore_poi]))

        superficy = {
            point: None if point in ignore_poi else 0
            for point in self.pois
        }

        for line in self.closest_raster:
            for col in line:
                if len(col) == 1:
                    # Ignore the points that are equidistant to multiple POI
                    point = col[0]
                    if superficy[point] is not None:
                        # Superficy count is None if they are on the edge
                        superficy[point] += 1

        return sorted([
            Zone(k, v) for k, v in superficy.items()
        ], key=lambda v: v.area if v.area is not None else -1, reverse=True)

    def common_zone(self, max_dist: int):
        self._populate_rasters()
        print('Looking for common zone within a distance of %d' % max_dist)

        interesting_points = []

        for y, line in enumerate(self.distance_raster):
            for x, col in enumerate(line):
                if col < max_dist:
                    interesting_points.append(Point(self.first_point.x + x, self.first_point.y + y, self))

        return interesting_points

    @property
    def first_point(self):  # -> Point
        if not self.pois:
            raise ValueError('No points of interests')
        return self.pois[0]

    @classmethod
    def from_file(cls, filename: str):  # -> Map
        coordinates = []

        mins = None
        maxs = None

        with open(filename) as f:
            for l in f.readlines():
                p = Point(*[int(p) for p in l.replace(' ', '').rstrip().split(',')])

                coordinates.append(p)

                if mins is None:
                    mins = Point(p.x, p.y)
                    maxs = Point(p.x, p.y)
                else:
                    mins.x = min(mins.x, p.x)
                    mins.y = min(mins.y, p.y)
                    maxs.x = max(maxs.x, p.x)
                    maxs.y = max(maxs.y, p.y)

        print('Loading %d coordinates from %s (zone from %s to %s)' % (
            len(coordinates),
            filename,
            str(mins),
            str(maxs),
        ))

        assert mins.x >= 0
        assert mins.y >= 0

        width = maxs.x - mins.x + 1
        height = maxs.y - mins.y + 1

        return cls(
            coordinates,
            mins,
            width,
            height
        )


if '__main__' == __name__:

    coordinates = Map.from_file('input.txt')

    print('Computing biggest zone within %d' % (coordinates.width * coordinates.height))
    biggest = coordinates.danger_zones()[0]

    print('Biggest (non-infinite) zone is from point %s and covers an area of %d.' % (
        str(biggest.point), biggest.area
    ))  # 3260

    dist = 10000
    common_zone = coordinates.common_zone(dist)
    print('Safest zone with %d of all points is an area of %d.' % (dist, len(common_zone)))
    # 42535
