
import math
import random
import pprint

import airmash.maps.world
import a_star


#board_width_px = 30912
#board_height_px = 14666

board_width_px = 32768
board_height_px = 16384

if 0:
    board_width_px = 50*4
    board_height_px = 50*4

tile_size = 50

board_width = int(math.ceil(board_width_px / tile_size))
board_height = int(math.ceil(board_height_px / tile_size))
print(['width', board_width, 'height', board_height])


bad = set()
# Top and bottom border.
bad.update((x, y)
           for y in (-1, board_height)
           for x in range(-1, 1+board_width))
# Left and right border.
bad.update((x, y)
           for x in (-1, board_width)
           for y in range(-1, 1+board_height))

if 0:
    bad.update(
        (random.randint(0, board_width),
         random.randint(0, board_height))
        for x in range(int(
            (board_width * board_height) * 0.2
        ))
    )

if 0:
    bad.update(
        (i, board_height//2)
        for i in range(1, board_width-1)
    )
    print('bad y=', board_height//2)


def neighbours(xy):
    x, y = xy
    for dx, dy in ((-1, -1),   # top left
                   (+0, -1),   # top middle
                   (+1, -1),   # top right
                   (-1, +0),   # middle left
                   (+1, +0),   # middle right
                   (-1, +1),   # bottom left
                   (+0, +1),   # bottom middle
                   (+1, +1)):  # bottom right
        t = x+dx, y+dy
        if t not in bad:
            yield t


def dist(xy1, xy2):
    if 1:
        x1, y1 = xy1
        x2 ,y2 = xy2
        return abs(x1 - x2) + abs(y1 - y2)
    else:
        return math.sqrt(
            ((xy1[0] - xy2[0]) ** 2) +
            ((xy1[1] - xy2[1]) ** 2)
        )


def go2():
    return a_star.astar(
        start=(1, 1),
        goal=(board_width-1, board_height-1),
        neighbours=neighbours,
        cost_estimate=dist,
    )



class Point:
    def __repr__(self):
        return 'Point(x=%r, y=%r)' % (
            self.x,
            self.y,
        )

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Circle:
    def __repr__(self):
        return 'Circle(%r, r=%r)' % (
            self.p,
            self.r,
        )

    def __init__(self, p, r):
        self.p = p
        self.r = r

    def as_bbox(self):
        return Box(
            p=Point(
                x=(self.p.x - self.r),
                y=(self.p.y - self.r),
            ),
            w=(self.r * 2),
            h=(self.r * 2),
        )

    def contains_point(self, p):
        dx = self.p.x - p.x
        dy = self.p.y - p.y
        return ((dx * dx) + (dy * dy)) < (self.r * self.r)

    def intersects_box(self, box):
        return self.contains_point(
            box.nearest_point_to(self.p)
        )


class Box:
    def __repr__(self):
        return 'Box(%r, %r, w=%r, h=%r)' % (
            self.p.x,
            self.p.y,
            self.w,
            self.h,
        )

    def __init__(self, p, w, h):
        self.p = p
        self.w = w
        self.h = h

    def nearest_point_to(self, p):
        return Point(
            x=max(self.p.x, min(p.x, self.p.x + self.w)),
            y=max(self.p.y, min(p.y, self.p.y + self.h)),
        )

    @property
    def bottom(self):
        return self.p.y + self.h

    @property
    def right(self):
        return self.p.x + self.w


def cap(n, c):
    return int(c * round(float(n)/c))


def circle_intersects(c, grid_size):
    r = c.as_bbox()
    for y in range(cap(r.p.y, grid_size),
                   cap(r.bottom, grid_size),
                   grid_size):
        for x in range(cap(r.p.x, grid_size),
                       cap(r.right, grid_size),
                       grid_size):
            b = Box(Point(x, y), grid_size, grid_size)
            if c.intersects_box(b):
                yield b


def get_bad_boxes():
    for x, y, r in airmash.maps.world.walls:
        yield from circle_intersects(Circle(Point(x, y), r), tile_size)

if 1:
    bad.update((b.p.x, b.p.y) for b in get_bad_boxes())


if 0:
    import sys
    print(list(circle_intersects(Circle(Point(2, 2), 2), 1)))
    for i, (x, y, does) in enumerate(circle_intersects(Circle(Point(100, 100), 100), 1)):
        if x == 0:
            sys.stdout.write('\n')
        sys.stdout.write('x' if does else '.')
    sys.stdout.write('\n')


if 1:
    print(go2())
    print('goal = ', (board_width-1, board_height-1))

if 0:
    for x in range(100):
        (go2())

import sys
#sys.exit(0)


if 0:
    cost, steps = go()
    pprint.pprint({
        'cost': cost,
        'nsteps': len(steps),
        'steps': steps,
    })
