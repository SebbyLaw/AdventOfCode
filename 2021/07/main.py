from util import *

@test(37)
def p1(f: Input):
    crabs = list(map(int, f.raw.split(',')))
    lowest = 1289371670421673467129496781346789
    for i in range(min(crabs), max(crabs)):
        total = sum(abs(c - i) for c in crabs)
        if total < lowest:
            lowest = total
    return lowest

def fuel_use(m: int):
    return sum(range(m + 1))

@test(168)
def p2(f: Input):
    crabs = list(map(int, f.raw.split(',')))
    lowest = 1289371670421673467129496781346789
    for i in range(min(crabs), max(crabs)):
        total = sum(fuel_use(abs(c - i)) for c in crabs)
        if total < lowest:
            lowest = total
    return lowest
