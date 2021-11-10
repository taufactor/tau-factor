import copy
import logging
import re
import typing

from bs4.element import Tag

from syllabus import defines as syllabus_scanner_defines
from syllabus import non_persistent_models as syllabus_scanner_non_persistent_models
from syllabus import utils as syllabus_scanner_utils

_logger = logging.getLogger(__name__)


class SyllabusPageParser:
    def __init__(self, body: Tag):
        self.body = body

        self._year: typing.Optional[int] = None
        self._courses: typing.Dict[str, syllabus_scanner_non_persistent_models.CourseInfo] = {}

    def parse(self) -> None:
        for course_first_row in self.body.find_all("tr", attrs={"class": "listtds"}):
            self._add_course_group(self._parse_course_group(course_first_row))

    def _add_course_group(self, course_group_info: syllabus_scanner_non_persistent_models.CourseGroupInfo) -> None:
        if course_group_info.course_code in self._courses:
            self._courses[course_group_info.course_code].course_groups.append(course_group_info)
        else:
            self._courses[course_group_info.course_code] = syllabus_scanner_non_persistent_models.CourseInfo(
                course_code=course_group_info.course_code,
                year=self.year,
                course_groups=[course_group_info],
            )

    @property
    def courses(self) -> typing.Tuple[syllabus_scanner_non_persistent_models.CourseInfo, ...]:
        return tuple(self._courses.values())

    @property
    def year(self) -> int:
        if self._year is not None:
            return self._year

        year_cell = self.body.select_one(".listtdbbld")
        if year_cell is None:
            _logger.error("Could not find year cell to parse.")
            raise ValueError("Could not find year cell to parse.")
        year_text = year_cell.text.strip()
        year_result = re.search(syllabus_scanner_defines.YEAR_PATTERN, year_text)
        if year_result is None:
            _logger.error("Could not parse year_text: \"%s\".", year_text)
            raise ValueError(F"Could not parse year_text: \"{year_text}\".")
        self._year = int(year_result[1])
        return self._year

    def _parse_course_group(self, course_first_row: Tag) -> syllabus_scanner_non_persistent_models.CourseGroupInfo:
        course_main_info_row = course_first_row.next_sibling
        if not course_main_info_row:
            _logger.error("Expected course_first_row to have a sibling row.")
            raise ValueError("Expected course_first_row to have a sibling row.")

        course_school_info_row = course_main_info_row.next_sibling
        if not course_school_info_row:
            _logger.error("Expected course_main_info_row to have a sibling row.")
            raise ValueError("Expected course_main_info_row to have a sibling row.")

        course_meetings_titles_row = course_school_info_row.next_sibling
        if not course_meetings_titles_row:
            _logger.error("Expected course_school_info_row to have a sibling row.")
            raise ValueError("Expected course_school_info_row to have a sibling row.")

        meetings_rows = []
        row = course_meetings_titles_row.next_sibling
        while row and not self._is_final_row_in_course(row):
            meetings_rows.append(row)
            row = row.next_sibling

        course_code, course_group_name, course_name = self._parse_course_main_info(course_main_info_row)
        faculty, school = self._parse_course_school_info(course_school_info_row)

        try:
            course_group_meetings = self._parse_course_group_meetings(meetings_rows)
        except ValueError:
            _logger.exception("Failed to parse meetings for %s-%s.", course_code, course_group_name)
            raise

        return syllabus_scanner_non_persistent_models.CourseGroupInfo(
            course_code=course_code,
            course_name=course_name,
            course_group_name=course_group_name,
            faculty=faculty,
            school=school,
            meetings=course_group_meetings,
        )

    @staticmethod
    def _is_final_row_in_course(row: Tag) -> bool:
        return "border-bottom" in row.attrs.get("style", "")

    @staticmethod
    def _parse_course_main_info(course_main_info_row: Tag) -> typing.Tuple[str, str, str]:
        course_main_info_cells = syllabus_scanner_utils.get_cells(
            course_main_info_row=course_main_info_row,
            num_expected_cells=2,
        )

        course_and_group_text = syllabus_scanner_utils.normalize(course_main_info_cells[0].text)
        course_and_group_result = re.search(syllabus_scanner_defines.COURSE_AND_GROUP_PATTERN, course_and_group_text)
        if not course_and_group_result:
            _logger.error("Could not parse course_and_group_text: \"%s\".", course_and_group_text)
            raise ValueError(F"Could not parse course_and_group_text: \"{course_and_group_text}\".")
        course_code = course_and_group_result[1]
        course_group = course_and_group_result[2]

        course_name = syllabus_scanner_utils.normalize(course_main_info_cells[1].text)
        return course_code, course_group, course_name

    @staticmethod
    def _parse_course_school_info(course_school_info_row: Tag) -> typing.Tuple[str, str]:
        course_school_info_cells = syllabus_scanner_utils.get_cells(
            course_school_info_row=course_school_info_row,
            num_expected_cells=2,
        )

        faculty_and_school_text = syllabus_scanner_utils.normalize(course_school_info_cells[1].text)
        faculty_and_school_result = re.search(
            pattern=syllabus_scanner_defines.FACULTY_AND_SCHOOL_PATTERN,
            string=faculty_and_school_text,
        )
        if not faculty_and_school_result:
            _logger.error("Could not parse faculty_and_school_text: \"%s\".", faculty_and_school_text)
            raise ValueError(F"Could not parse faculty_and_school_text: \"{faculty_and_school_text}\".")
        faculty = faculty_and_school_result[1]
        school = faculty_and_school_result[2]
        return faculty, school

    @staticmethod
    def _parse_course_meeting_with_full_data(
            course_meeting_cells: typing.Sequence[Tag],
            last_course_group_meeting: typing.Optional[syllabus_scanner_non_persistent_models.CourseGroupMeetingInfo],
    ) -> syllabus_scanner_non_persistent_models.CourseGroupMeetingInfo:
        teacher_name_text = syllabus_scanner_utils.normalize(course_meeting_cells[0].text)
        meeting_type = syllabus_scanner_non_persistent_models.MeetingType.from_text(
            text=syllabus_scanner_utils.normalize(course_meeting_cells[1].text),
        )
        building = syllabus_scanner_utils.normalize(course_meeting_cells[2].text) or None
        room = syllabus_scanner_utils.normalize(course_meeting_cells[3].text) or None
        day_text = syllabus_scanner_utils.normalize(course_meeting_cells[4].text)
        hours_list = syllabus_scanner_utils.normalize(course_meeting_cells[5].text).split("-")
        semester = syllabus_scanner_non_persistent_models.Semester.from_text(
            text=syllabus_scanner_utils.normalize(course_meeting_cells[6].text),
        )

        day = syllabus_scanner_non_persistent_models.Day.from_text(day_text) if day_text else None
        starting_time = hours_list[0] if len(hours_list) == 2 else None
        ending_time = hours_list[1] if len(hours_list) == 2 else None

        if day is None and (starting_time is not None or ending_time is not None):
            _logger.error(
                "Course group has no day set but starting_time=%s or ending_time=%s are set.",
                starting_time,
                ending_time,
            )
            raise ValueError(
                F"Course group has no day set but starting_time={starting_time} or ending_time={ending_time} are set.",
            )

        if teacher_name_text:
            teachers = {syllabus_scanner_non_persistent_models.Teacher.from_text(teacher_name_text)}
        elif last_course_group_meeting and last_course_group_meeting.teachers:
            teachers = copy.copy(last_course_group_meeting.teachers)
        else:
            teachers = set()

        return syllabus_scanner_non_persistent_models.CourseGroupMeetingInfo(
            meeting_type=meeting_type,
            teachers=teachers,
            semester=semester,
            building=building,
            room=room,
            day=day,
            starting_time=starting_time,
            ending_time=ending_time,
        )

    @staticmethod
    def _parse_course_meeting_with_partial_data(
            course_meeting_cells: typing.Sequence[Tag],
            last_course_group_meeting: typing.Optional[syllabus_scanner_non_persistent_models.CourseGroupMeetingInfo],
    ) -> None:
        """
        Parses a row of a specific meeting in a course group instance, when the row consists only of the
        teacher name. This happens whenever a meeting has more than one teacher.
        In this case we just add the teacher to the last parsed meeting
        :param course_meeting_cells: The cells of the meeting row being processed.
        :param last_course_group_meeting: The last meeting that was processed, if exists.
        :returns: Nothing
        """
        teacher_name_text = syllabus_scanner_utils.normalize(course_meeting_cells[0].text)
        empty_cell = syllabus_scanner_utils.normalize(course_meeting_cells[1].text)
        if empty_cell:
            _logger.error("Expected row to have only the teacher name, but got also %s.", empty_cell)
            raise ValueError(F"Expected row to have only the teacher name, but got also {empty_cell}.")

        if not last_course_group_meeting:
            _logger.error("Partial meeting rows are expected only after parsing a full meeting row.")
            raise ValueError("Partial meeting rows are expected only after parsing a full meeting row.")

        if teacher_name_text:
            last_course_group_meeting.teachers.add(
                syllabus_scanner_non_persistent_models.Teacher.from_text(teacher_name_text),
            )

    def _parse_course_group_meetings(
            self,
            course_meetings_rows: typing.Iterable[Tag],
    ) -> typing.Tuple[syllabus_scanner_non_persistent_models.CourseGroupMeetingInfo, ...]:
        course_group_meetings: typing.List[syllabus_scanner_non_persistent_models.CourseGroupMeetingInfo] = []

        course_group_meeting: typing.Optional[syllabus_scanner_non_persistent_models.CourseGroupMeetingInfo] = None
        for course_meeting_row in course_meetings_rows:
            course_meeting_cells = syllabus_scanner_utils.get_cells(course_meeting_row=course_meeting_row)
            num_course_meeting_cells = len(course_meeting_cells)
            if num_course_meeting_cells == 7:
                course_group_meeting = self._parse_course_meeting_with_full_data(
                    course_meeting_cells=course_meeting_cells,
                    last_course_group_meeting=course_group_meeting,
                )
                course_group_meetings.append(course_group_meeting)
            elif num_course_meeting_cells == 2:
                self._parse_course_meeting_with_partial_data(
                    course_meeting_cells=course_meeting_cells,
                    last_course_group_meeting=course_group_meeting,
                )
            else:
                _logger.error("Unexpected meeting row with %s cells.", num_course_meeting_cells)
                raise ValueError(F"Unexpected meeting row with {num_course_meeting_cells} cells.")

        return tuple(course_group_meetings)
