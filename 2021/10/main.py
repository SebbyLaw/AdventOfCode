from util import *
import statistics

pairs = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

@test(26397)
def p1(inp: Input):
    openings = []
    total = 0
    for line in inp:
        for char in line:
            if char in pairs:
                openings.append(char)
            else:
                expected = pairs[openings[-1]]
                if expected == char:
                    openings.pop()
                else:
                    total += points[char]
                    break

    return total


points2 = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


@test(288957)
def p2(inp: Input):
    bad = set()
    scores = []
    for i, line in enumerate(inp):
        openings = []
        for char in line:
            if char in pairs:
                openings.append(char)
            else:
                expected = pairs[openings[-1]]
                if expected == char:
                    openings.pop()
                else:
                    bad.add(i)
                    break

        if i in bad:  # lol
            continue

        completion = []
        for char in reversed(openings):
            com = pairs[char]
            completion.append(com)

        score = 0
        # calculate score
        for char in completion:
            score *= 5
            score += points2[char]

        scores.append(score)

    return statistics.median(scores)
