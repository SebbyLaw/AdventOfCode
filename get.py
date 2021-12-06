import datetime

import aiohttp
import discord

from util import get_session

URL_FMT: str = "https://adventofcode.com/{YEAR}/day/{DAY}/input"

# AOC timezone: UTC-5
timezone = datetime.timezone(datetime.timedelta(hours=-5))


def get_date(day: int, year: int) -> datetime.datetime:
    return datetime.datetime(year, 12, day, 0, 0, 1, tzinfo=timezone)


async def pull(day: int, year: int) -> None:
    date = get_date(day=day, year=year)
    print(f"Sleeping until {date}")
    await discord.utils.sleep_until(date)

    session = get_session()
    resp: aiohttp.ClientResponse = await session.get(URL_FMT.format(DAY=day, YEAR=year))
    with open(f'{year}/{day:02}/input', 'wb') as inp:
        inp.write(await resp.read())

    await session.close()


if __name__ == '__main__':
    import asyncio

    today = datetime.datetime.now(tz=timezone)
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(pull(day=today.day + 1, year=today.year))
