import asyncio
import logging
import typing

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from bs4.element import Tag

from syllabus import defines as syllabus_scanner_defines
from syllabus import non_persistent_models as syllabus_scanner_non_persistent_models

_logger = logging.getLogger(__name__)


class SyllabusLoader:
    def __init__(self, year: int):
        self._year = year
        self.queue = asyncio.Queue(maxsize=syllabus_scanner_defines.PAGE_QUEUE_SIZE)
        self.consumer: typing.Optional[asyncio.Task] = None

    async def _load_syllabus_pages(self, dep: str) -> None:
        async with ClientSession(headers=syllabus_scanner_defines.HEADERS) as session:
            page_number = 1
            first_page = await self._get_first_page(session=session, dep=dep)
            parsed_page = BeautifulSoup(first_page, features="html.parser")
            parsed_body = parsed_page.body
            if parsed_body is None:
                raise ValueError(F"Page number {page_number} does not have a body.")

            page_entry = syllabus_scanner_non_persistent_models.PageEntry(
                dep=dep,
                page_number=page_number,
                body=parsed_body,
            )
            await self.queue.put(page_entry)
            _logger.debug("Loaded page %s for Dep %s.", page_number, dep)

            while True:
                next_page = await self._get_next_page(session=session, body=parsed_body)
                if next_page is None:
                    break
                page_number += 1
                parsed_page = BeautifulSoup(next_page, features="html.parser")
                parsed_body = parsed_page.body
                if parsed_body is None:
                    raise ValueError(F"Page number {page_number} does not have a body.")

                page_entry = syllabus_scanner_non_persistent_models.PageEntry(
                    dep=dep,
                    page_number=page_number,
                    body=parsed_body,
                )
                await self.queue.put(page_entry)
                _logger.debug("Loaded page %s for Dep %s.", page_number, dep)

            empty_page = syllabus_scanner_non_persistent_models.PageEntry(
                dep=dep,
                page_number=-1,
                body=None,
            )
            await self.queue.put(empty_page)

    async def _get_first_page(self, session: ClientSession, dep: str) -> bytes:
        async with session.post(
            url=syllabus_scanner_defines.URL,
            data={
                "lstYear1": str(self._year),
                "lstDep1": dep,
                "ckYom": ["1", "2", "3", "4", "5", "6"],
            },
        ) as response:
            if response.status != 200:
                raise ValueError(F"Failed to fetch first syllabus page. status_code={response.status}")
            return await response.read()

    @staticmethod
    async def _get_next_page(session: ClientSession, body: Tag) -> typing.Optional[bytes]:
        if not body.find("input", attrs={"id": "next"}):
            return None

        form = body.find("form", attrs={"id": "frmgrid"})
        method = form.attrs["method"].upper()
        params = {
            "__VIEWSTATE": form.find("input", attrs={"id": "__VIEWSTATE"}).attrs["value"],
            "__EVENTVALIDATION": form.find("input", attrs={"id": "__EVENTVALIDATION"}).attrs["value"],
            "dir1": "1",
        }

        async with session.request(
            method=method,
            url=syllabus_scanner_defines.URL,
            data=params,
        ) as response:
            if response.status != 200:
                raise ValueError(F"Failed to fetch next syllabus page. status_code={response.status}")
            return await response.read()

    def set_consumer(self, consumer: typing.Callable[[asyncio.Queue], typing.Coroutine]) -> None:
        loop = asyncio.get_event_loop()
        self.consumer = loop.create_task(consumer(self.queue))

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.wait((
                self._run(),
            )),
        )

    async def _run(self):
        loop = asyncio.get_event_loop()
        producer_tasks = tuple(
            loop.create_task(self._load_syllabus_pages(dep))
            for dep in syllabus_scanner_defines.DEPS_TO_LOAD
        )
        await asyncio.wait(producer_tasks)
        await self.queue.join()
