import itertools
from collections import Counter

from util import *


# lol im not on 3.10
def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


@test(1588)
def p1(inp: Input):
    starting, ins = inp.chunks

    starting: str
    ins: Dict[str, str] = {v[0]: v[1] for v in (s.split(' -> ') for s in ins.splitlines())}

    for i in range(10):
        insertions = []
        tmp = []
        for pair in pairwise(starting):
            insertions.append(ins[''.join(pair)])
        for s, p in zip(starting, insertions):
            tmp.append(s)
            tmp.append(p)
        starting = ''.join(tmp) + starting[-1]

    c = Counter(starting)
    mc = c.most_common()
    return mc[0][1] - mc[-1][1]  # thanks oli


@test(2188189693529)
def p2(inp: Input):
    starting, ins = inp.chunks
    starting: str
    ins: Dict[str, str] = {v[0]: v[1] for v in (s.split(' -> ') for s in ins.splitlines())}
    resulting: Dict[str, Tuple[str, str, str]] = {
        inst: (f'{inst[0]}{res}', f'{res}{inst[1]}', res)
        for inst, res in ins.items()
    }

    c = Counter(starting)
    pairs = Counter(''.join(h) for h in pairwise(starting))
    for i in range(40):
        np = Counter()
        for p, n in pairs.items():
            p1, p2, rs = resulting[p]
            np[p1] += n
            np[p2] += n
            c[rs] += n
        pairs = np

    mc = c.most_common()
    return mc[0][1] - mc[-1][1]  # thanks oli
