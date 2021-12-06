import asyncio
import datetime
import logging
import re
from html.parser import HTMLParser
from typing import Union, List, Tuple

import aiohttp
import discord

from util import get_session

log = logging.getLogger()

URL_FMT: str = "https://adventofcode.com/{YEAR}/day/{DAY}"

# AOC timezone: UTC-5
timezone = datetime.timezone(datetime.timedelta(hours=-5))


async def sleep_until_ready(day: int, year: int) -> None:
    date = datetime.datetime(year, 12, day, 0, 0, 1, tzinfo=timezone)
    log.debug(f"Sleeping until {date}")
    await discord.utils.sleep_until(date)


async def pull_input(day: int, year: int, session: aiohttp.ClientSession) -> None:
    await sleep_until_ready(day=day, year=year)

    resp: aiohttp.ClientResponse = await session.get(URL_FMT.format(DAY=day, YEAR=year) + '/input')
    with open(f'{year}/{day:02}/input', 'wb') as inp:
        inp.write(await resp.read())

    log.info("Successfully fetched today's input!")


class AOCParser(HTMLParser):
    """
    As far as I can tell, the example input is always within a <code>
    preceded by a <p> that includes the text "For example" in some form.

    This parser tries to (badly) parse out the example input.
    """
    FOR_EXAMPLE = re.compile(r"for example", flags=re.IGNORECASE)

    def __init__(self):
        super().__init__()
        self.curr_tag: str = ''
        self.example_found: bool = False
        self._example: str = ''

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Union[str, None]]]) -> None:
        self.curr_tag = tag

    def handle_data(self, data: str) -> None:
        if self.curr_tag == 'p':
            if self.FOR_EXAMPLE.search(data) is not None:
                self.example_found = True
        elif self.curr_tag == 'code':
            if self.example_found:
                self._example = data
                self.example_found = False

    @property
    def test_case(self) -> str:
        return self._example


def parse_input_html(raw: bytes) -> str:
    """Hopefully parse out the test input."""
    parser = AOCParser()
    parser.feed(raw.decode('utf-8'))
    parser.close()
    return parser.test_case


async def pull_test_input(day: int, year: int, session: aiohttp.ClientSession) -> None:
    await sleep_until_ready(day=day, year=year)

    resp: aiohttp.ClientResponse = await session.get(URL_FMT.format(DAY=day, YEAR=year))

    test_case = parse_input_html(await resp.read())

    with open(f'{year}/{day:02}/test', 'w') as f:
        f.write(test_case)

    log.info("Successfully fetched today's test input!")

async def main() -> None:
    session = get_session()
    today = datetime.datetime.now(tz=timezone)
    # add 1 day here, so we can use this script on the first day (November 30)
    today += datetime.timedelta(days=1)

    tasks = [
        pull_input(day=today.day, year=today.year, session=session),
        pull_test_input(day=today.day, year=today.year, session=session),
    ]

    try:
        await asyncio.gather(*tasks)
    finally:
        await session.close()


if __name__ == '__main__':
    # log.setLevel(logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
