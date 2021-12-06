import typing

import aiohttp


__all__ = (
    'get_session',
)


def get_session() -> aiohttp.ClientSession:
    with open('.session', 'r') as f:
        session = f.read().strip()

    cookies = {'session': session}
    return aiohttp.ClientSession(cookies=cookies)
