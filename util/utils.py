import typing
from typing import List, TypeVar

import aiohttp

T = TypeVar('T')
Func = typing.Callable[[typing.TextIO], typing.Any]

__all__ = (
    'get_session',
    'read',
    'run',
    'test',
)


def get_session() -> aiohttp.ClientSession:
    with open('.session', 'r') as f:
        session = f.read().strip()

    cookies = {'session': session}
    return aiohttp.ClientSession(cookies=cookies)


def read(t: T = int) -> List[T]:
    with open(f"input", 'r') as f:
        return [t(line.strip()) for line in f.readlines()]


def test(func: Func) -> Func:
    with open('test', 'r') as f:
        print(f'{func.__name__} Test Result:', func(f))
    return func


def run(func: Func) -> Func:
    with open('input', 'r') as f:
        print(f'{func.__name__} Input Result:', func(f))
    return func
