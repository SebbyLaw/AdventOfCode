from collections import *
from typing import *

from util import *


class Line:
    def __init__(self, s: str):
        k = s.split(' -> ')
        self.a = tuple(map(int, k[0].split(',')))
        self.b = tuple(map(int, k[1].split(',')))


x = 0
y = 1

@run
@test
def sol(f):
    lines: List[Line] = list(map(Line, f.readlines()))

    ch = lambda l: l.a[x] == l.b[x] or l.a[y] == l.b[y]

    co = Counter()

    for line in filter(ch, lines):
        if line.a[x] == line.b[x]:
            for i in range(min(line.a[y], line.b[y]), max(line.a[y], line.b[y]) + 1):
                co[(line.a[x], i)] += 1
        else:
            for i in range(min(line.a[x], line.b[x]), max(line.a[x], line.b[x]) + 1):
                co[(i, line.a[y])] += 1

    return sum(c >= 2 for c in co.values())


@run
@test
def sol2(f):
    # copy paste
    lines: List[Line] = list(map(Line, f.readlines()))

    ch = lambda l: l.a[x] == l.b[x] or l.a[y] == l.b[y]

    co = Counter()

    for line in filter(ch, lines):
        if line.a[x] == line.b[x]:
            for i in range(min(line.a[y], line.b[y]), max(line.a[y], line.b[y]) + 1):
                co[(line.a[x], i)] += 1
        else:
            for i in range(min(line.a[x], line.b[x]), max(line.a[x], line.b[x]) + 1):
                co[(i, line.a[y])] += 1

    for line in filter(lambda l: not ch(l), lines):
        xs = list(range(line.a[x], line.b[x] + (1 if line.a[x] < line.b[x] else -1), 1 if line.a[x] < line.b[x] else -1))
        ys = list(range(line.a[y], line.b[y] + (1 if line.a[y] < line.b[y] else -1), 1 if line.a[y] < line.b[y] else -1))

        for a in zip(xs, ys):
            co[a] += 1

    return sum(c >= 2 for c in co.values())
