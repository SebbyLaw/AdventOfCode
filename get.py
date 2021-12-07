import asyncio
import datetime
import logging
import re
from html.parser import HTMLParser
from typing import List, Tuple, Union

import aiohttp
import discord

from util.web import get_session, now, timezone, URL_FMT

log = logging.getLogger()


async def sleep_until_ready(day: int, year: int) -> None:
    date = datetime.datetime(year, 12, day, 0, 0, 15, tzinfo=timezone)
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
        self.curr: List[str] = []
        self.example_found: bool = False
        self._example: str = ''

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Union[str, None]]]) -> None:
        self.curr.append(tag)

    def handle_data(self, data: str) -> None:
        if not self.curr:
            return

        if 'p' in self.curr:
            if self.FOR_EXAMPLE.search(data) is not None:
                self.example_found = True
                return
        if self.curr[-1] == 'code':
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

    with open(f'{year}/{day:02}/test', 'wb') as f:
        f.write(test_case.encode('utf-8'))

    log.info("Successfully fetched today's test input!")

async def main(day: int = None) -> None:
    session = get_session()
    # add 1 day here, so we can use this script on the first day (November 30)
    if day is None:
        today = now() + datetime.timedelta(days=1)
    else:
        today = now().replace(day=day)

    tasks = [
        pull_input(day=today.day, year=today.year, session=session),
        pull_test_input(day=today.day, year=today.year, session=session),
    ]

    try:
        await asyncio.gather(*tasks)
    finally:
        await session.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
