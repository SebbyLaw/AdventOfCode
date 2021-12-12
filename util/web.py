import datetime

import aiohttp

__all__ = (
    'get_session',
    'now',
    'timezone',
    'URL_FMT',
)

URL_FMT: str = "https://adventofcode.com/{YEAR}/day/{DAY}"
# AOC timezone: UTC-5
timezone = datetime.timezone(datetime.timedelta(hours=-5))


def now() -> datetime.datetime:
    """
    "Now" but in UTC-5
    """
    return datetime.datetime.now(tz=timezone)


def get_session() -> aiohttp.ClientSession:
    with open('.session', 'r') as f:
        session = f.read().strip()

    cookies = {'session': session}
    return aiohttp.ClientSession(cookies=cookies)
