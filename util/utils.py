from typing import List, TypeVar

T = TypeVar('T')

__all__ = (
    'read',
)

def read(t: T = int) -> List[T]:
    with open(f"input", 'r') as f:
        return [t(line.strip()) for line in f.readlines()]
