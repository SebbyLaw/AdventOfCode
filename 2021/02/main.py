from util.old import read

class Step:
    def __init__(self, s):
        self.d, self.x = s.split(' ')
        self.x = int(self.x)

def sol(inp):
    depth = 0
    pos = 0
    for s in inp:
        if s.d == 'forward':
            pos += s.x
        if s.d == 'down':
            depth += s.x
        if s.d == 'up':
            depth -= s.x

    return depth * pos

def sol2(inp):
    depth = 0
    pos = 0
    aim = 0
    for s in inp:
        if s.d == 'forward':
            pos += s.x
            depth += (aim * s.x)
        if s.d == 'down':
            aim += s.x
        if s.d == 'up':
            aim -= s.x

    return depth * pos


if __name__ == '__main__':
    print(sol(read(Step)))
    print(sol2(read(Step)))
