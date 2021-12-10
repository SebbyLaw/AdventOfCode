import asyncio
import datetime
import importlib
import logging
import sys
import time
import traceback
from typing import Any, Literal, Optional

from util import Input, SolutionFunction
from util.web import now, get_session, URL_FMT

log = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


async def submit(day: int, year: int, level: Literal[1, 2], answer: Any):
    session = get_session()

    try:
        resp = await session.post(URL_FMT.format(DAY=day, YEAR=year) + '/answer', data={'level': level, 'answer': str(answer)})
        if resp.status != 200:
            print(await resp.text())
            raise
        else:
            pass
    finally:
        await session.close()


def run_solution(solution: SolutionFunction, inp: Input, expected_result: Any = None) -> Optional[bool]:
    try:
        before = time.perf_counter_ns()
        answer = solution(inp)
        after = time.perf_counter_ns()
    except:
        traceback.print_exc()
    else:
        name = solution.__name__
        length = after - before

        log.debug(f'[ {name}{"[test]" if expected_result is not None else ""} finished in {length}ns ({length / 1000000}ms) {"({} seconds)".format(length / 1000000000) if length > 1000000000 else ""} ]')
        if expected_result is not None:
            passed = expected_result == answer
            log.debug(f'[ {name} {"PASS" if passed else "FAIL"}: Expected {expected_result}, got {answer} ]')
            return passed
        else:
            print(f'{name}: {answer}')


async def main(day: int = None):
    if day is None:
        today = now()
    else:
        today = now().replace(day=day)

    module = importlib.import_module(f'{today.year}.{today.day:02}.main')

    try:
        p1: SolutionFunction = getattr(module, 'p1')
        p2: SolutionFunction = getattr(module, 'p2')
    except AttributeError:
        print("Solution functions not found")
        sys.exit(1)  # lol

    with open(f'{today.year}/{today.day:02}/test') as f:
        test_input: Input = Input(f)

    with open(f'{today.year}/{today.day:02}/input') as f:
        real_input: Input = Input(f)

    for i, f in enumerate((p1, p2), start=1):
        expected_result = getattr(f, '__aoc_test_expected_result__', None)
        if run_solution(f, test_input, expected_result):
            answer = run_solution(f, real_input)
            # await submit(day=today.day, year=today.year, level=i, answer=answer)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
