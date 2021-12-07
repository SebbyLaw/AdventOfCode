from typing import List, TextIO

__all__ = (
    'Input',
    'test',
)


def test(expected):
    def deco(func):
        func.__aoc_test_expected_result__ = expected
        return func
    return deco


class Input:
    def __init__(self, file: TextIO):
        self._raw: str = file.read().strip()

    @property
    def raw(self) -> str:
        return self._raw

    @property
    def lines(self) -> List[str]:
        return self._raw.splitlines(keepends=False)

    @property
    def chunks(self) -> List[str]:
        return self._raw.split('\n\n')
