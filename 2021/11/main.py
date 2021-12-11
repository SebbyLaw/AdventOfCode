import typing

from util import *


def flash(o: Node[int], flashed: typing.Set[typing.Tuple[int, int]]):
    if o.coord in flashed:
        return

    elif o.value > 9:
        flashed.add(o.coord)
        for i in o.adjacent():
            i.value += 1
            flash(i, flashed)


def step(octopuses: Grid[int]) -> int:
    flashed = set()

    for o in octopuses:
        o.value += 1

    for o in octopuses:
        flash(o, flashed)

    for o in octopuses:
        if o.val > 9:
            o.val = 0

    return len(flashed)


@test(1656)
def p1(inp: Input):
    octopuses = inp.grid(c=int, delimiter='')
    return sum(step(octopuses) for _ in range(100))


@test(195)
def p2(inp: Input):
    octopuses = inp.grid(c=int, delimiter='')
    ans = 0

    while True:
        ans += 1
        if step(octopuses) == len(octopuses):
            return ans
