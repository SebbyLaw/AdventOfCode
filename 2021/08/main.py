from typing import *

from util import *


@test(26)
def p1(inp: Input):
    c = 0

    for line in inp:
        last4 = line.split(" | ")[1].split(' ')
        for n in last4:
            if len(n) in (2, 4, 3, 7):
                c += 1

    return c


@test(61229)
def p2(inp: Input):
    total = 0
    # 1   C  F   (2) one       .
    # 7 A C  F   (3) seven     .
    # 4  BCD F   (4) four      .
    # 2 A CDE G  (5) two       .
    # 3 A CD FG  (5) three     .
    # 5 AB D FG  (5) five      .
    # 6 AB DEFG  (6) six       .
    # 9 ABCD FG  (6) nine      .
    # 0 ABC EFG  (6) zero      .
    # 8 ABCDEFG  (7) eight     .
    for line in inp:
        first: List[Set[str]]
        last: List[Set[str]]
        first, last = map(lambda s: [set(s) for s in s.split(' ')], line.split(' | '))
        first.sort(key=len)
        # known values by unique length
        one = first[0]
        seven = first[1]
        four = first[2]
        eight = first[-1]
        # three is the only len()==5 number that is a superset of one. (has both C and F)
        three = next(f for f in first if len(f) == 5 and f >= one)
        # B = (BCDF - ACDFG)
        b = (four - three).pop()
        # two is the only other len()==5 number without B
        two = next(f for f in first if len(f) == 5 and f != three and b not in f)
        # C is the only common segment between one two and three
        c = (one & two & three).pop()
        # five is the last len()==5 number
        five = next(f for f in first if len(f) == 5 and f not in (two, three))
        # E = (ACDEG - ACDFG - CF)
        e = (two - three - one).pop()
        # six is the only len()==6 number without C
        six = next(f for f in first if len(f) == 6 and c not in f)
        # nine is the only len()==6 number without E
        nine = next(f for f in first if len(f) == 6 and e not in f)
        # zero is the last len()==6 number
        zero = next(f for f in first if len(f) == 6 and f not in (six, nine))

        m = [zero, one, two, three, four, five, six, seven, eight, nine]
        for mod, s in enumerate(reversed(last)):
            for i, n in enumerate(m):
                if s == n:
                    total += i * 10 ** mod

    return total
