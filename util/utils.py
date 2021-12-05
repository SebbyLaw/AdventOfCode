import typing
from typing import List, TypeVar

T = TypeVar('T')
Func = typing.Callable[[typing.TextIO], typing.Any]

__all__ = (
    'read',
    'run',
    'test',
)

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
