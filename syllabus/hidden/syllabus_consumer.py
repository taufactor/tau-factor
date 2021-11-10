import asyncio
import logging
import typing

from syllabus import defines as syllabus_scanner_defines
from syllabus import non_persistent_models as syllabus_scanner_non_persistent_models
from syllabus import syllabus_page_parser

_logger = logging.getLogger(__name__)


class SyllabusConsumer:
    def __init__(self):
        self.courses: typing.Tuple[syllabus_scanner_non_persistent_models.CourseInfo, ...] = ()

    async def consumer(self, queue: asyncio.Queue) -> None:
        async for page_entry in self.pages(queue):
            _logger.debug("Processing page %s of dep %s.", page_entry.page_number, page_entry.dep)
            parser = syllabus_page_parser.SyllabusPageParser(body=page_entry.body)
            parser.parse()
            self.courses += parser.courses
            _logger.debug(
                "Done processing page %s of dep %s. Total number of courses is %s.",
                page_entry.page_number,
                page_entry.dep,
                len(self.courses),
            )
        _logger.info("Done processing all pages.")

    @staticmethod
    async def pages(queue: asyncio.Queue):
        expected_completions = len(syllabus_scanner_defines.DEPS_TO_LOAD)
        num_completions = 0
        while num_completions < expected_completions:
            page_entry: syllabus_scanner_non_persistent_models.PageEntry = await queue.get()
            if page_entry.is_valid:
                yield page_entry
            else:
                num_completions += 1
            queue.task_done()
