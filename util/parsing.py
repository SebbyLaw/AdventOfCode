from typing import List


__all__ = (
    'Input',
)

class Input:
    def __init__(self, filename: str = 'input'):
        with open(filename, 'r') as f:
            self._raw: str = f.read().strip()

    @property
    def raw(self) -> str:
        return self._raw

    @property
    def lines(self) -> List[str]:
        return self._raw.splitlines(keepends=False)

    @property
    def chunks(self) -> List[str]:
        return self._raw.split('\n\n')
