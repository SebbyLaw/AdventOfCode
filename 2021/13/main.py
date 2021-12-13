from util import *


def gprint(coords: Set[Coord]) -> str:
    s = ''
    for y in range(max(coords, key=lambda t: t[1])[1] + 1):
        for x in range(max(coords, key=lambda t: t[0])[0] + 1):
            if (x, y) in coords:
                s += '#'
            else:
                s += '.'
        s += '\n'

    return s.strip()


@test(17)
def p1(inp: Input):
    cords, instructions = (s.splitlines() for s in inp.chunks)
    coords: Set[Coord] = set(tuple(map(int, a.split(','))) for a in cords)  # type: ignore

    xy, n = instructions[0].split()[-1].split('=')
    n = int(n)
    rm = [c for c in coords if c[0 if xy == 'x' else 1] > n]

    coords.difference_update(rm)

    for r in rm:
        if xy == 'x':
            new_coord = (r[0] - 2 * (r[0] - n), r[1])
        else:
            new_coord = (r[0], r[1] - 2 * (r[1] - n))
        coords.add(new_coord)

    return len(coords)


@test("""#####
#...#
#...#
#...#
#####""")
def p2(inp: Input):
    cords, instructions = (s.splitlines() for s in inp.chunks)
    coords: Set[Coord] = set(tuple(map(int, a.split(','))) for a in cords)  # type: ignore

    for st in instructions:
        xy, n = st.split()[-1].split('=')
        n = int(n)
        rm = [c for c in coords if c[0 if xy == 'x' else 1] > n]

        coords.difference_update(rm)

        for r in rm:
            if xy == 'x':
                new_coord = (r[0] - 2 * (r[0] - n), r[1])
            else:
                new_coord = (r[0], r[1] - 2 * (r[1] - n))
            coords.add(new_coord)

    s = gprint(coords)
    print(s.replace('.', ' '))
    return s
