__all__ = (
    'AOCError',
    'NoPathPossible',
)


class AOCError(Exception):
    pass


class NoPathPossible(AOCError):
    pass
