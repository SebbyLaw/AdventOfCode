from collections import *
from util import *


def cycle(fish, n):
    nlist = []
    c = 0
    if n == 0:
        return fish
    for f in fish:
        if f == 0:
            nlist.append(6)
            c += 1
        else:
            nlist.append(f-1)
    nlist.extend([8]*c)
    return cycle(nlist, n-1)

@test
@run
def p1(f):
    nums = list(map(int, f.read().split(',')))
    return len(cycle(nums, 80))


def cycle2(fish, n):
    if n == 0:
        return fish

    c = Counter()
    for i in range(1, 9):
        c[i-1] = fish[i]

    c[6] += fish[0]
    c[8] += fish[0]

    return cycle2(c, n-1)


@test
@run
def p2(f):
    nums = list(map(int, f.read().split(',')))
    c = Counter()
    for i in range(0, 9):
        c[i] += sum(i == n for n in nums)

    return sum(cycle2(c, 256).values())

