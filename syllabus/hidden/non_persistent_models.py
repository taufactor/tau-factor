import enum
import logging
import typing

from bs4.element import Tag

_logger = logging.getLogger(__name__)


class PageEntry(typing.NamedTuple):
    dep: str
    page_number: int
    body: typing.Optional[Tag]

    @property
    def is_valid(self) -> bool:
        return self.body is not None


class Semester(enum.Enum):
    a = "A"
    b = "B"
    all_year = "All Year"  # Deduced
    summer = "Summer"

    @staticmethod
    def from_text(text: str) -> "Semester":
        text_to_semester_mapping = {
            "א'": Semester.a,
            "ב'": Semester.b,
            "קיץ": Semester.summer,
        }
        semester = text_to_semester_mapping.get(text)
        if semester is None:
            _logger.error("Got a Unexpected semester %s.", text)
            raise ValueError(F"Got a Unexpected semester {text}.")
        return semester


class MeetingType(enum.Enum):
    lecture = "Lecture"
    exercise = "Exercise"
    lecture_and_exercise = "Lecture and Exercise"
    lecture_and_laboratory = "Lecture and Laboratory"
    project = "Project"
    workshop = "Workshop"
    seminar = "Seminar"
    seminar_paper = "Seminar Paper"
    proseminar = "Proseminar"
    practicum = "Practicum"
    laboratory = "Laboratory"
    field_trip = "Field Trip"
    personal_training = "Personal Training"
    bibliography_tutorial = "Bibliography Tutorial"
    guided_readings = "Guided Readings"

    @staticmethod
    def from_text(text: str) -> "MeetingType":
        text_to_meeting_type_mapping = {
            "שיעור": MeetingType.lecture,
            "תרגיל": MeetingType.exercise,
            "שיעור ותרגיל": MeetingType.lecture_and_exercise,
            "שיעור ומעבדה": MeetingType.lecture_and_laboratory,
            "פרוייקט": MeetingType.project,
            "סדנה": MeetingType.workshop,
            "סמינר": MeetingType.seminar,
            "פרוסמינר": MeetingType.proseminar,
            "עבודה סמינריונית": MeetingType.seminar_paper,
            "עבודה מעשית": MeetingType.practicum,
            "קולוקויום": MeetingType.seminar,
            "מעבדה": MeetingType.laboratory,
            "סיור": MeetingType.field_trip,
            "הדרכה אישית": MeetingType.personal_training,
            "הדרכה ביבליוגרפית": MeetingType.bibliography_tutorial,
            "קריאה מודרכת": MeetingType.guided_readings,
        }
        meeting_type = text_to_meeting_type_mapping.get(text)
        if meeting_type is None:
            _logger.error("Got a Unexpected meeting type %s.", text)
            raise ValueError(F"Got a Unexpected meeting type {text}.")
        return meeting_type


class Day(enum.Enum):
    sunday = "Sunday"
    monday = "Monday"
    tuesday = "Tuesday"
    wednesday = "Wednesday"
    thursday = "Thursday"
    friday = "Friday"

    @staticmethod
    def from_text(text: str) -> "Day":
        text_to_day_mapping = {
            "א": Day.sunday,
            "ב": Day.monday,
            "ג": Day.tuesday,
            "ד": Day.wednesday,
            "ה": Day.thursday,
            "ו": Day.friday,
        }
        day = text_to_day_mapping.get(text)
        if day is None:
            _logger.error("Got a Unexpected day %s.", text)
            raise ValueError(F"Got a Unexpected day {text}.")
        return day


class Teacher(typing.NamedTuple):
    honorific: str
    full_name: str

    @classmethod
    def from_text(cls, teacher_name_text: str) -> "Teacher":
        return Teacher(
            honorific=teacher_name_text.split(" ")[0],
            full_name=teacher_name_text.split(" ", 1)[1],
        )

    def __str__(self):
        return F"{self.honorific} {self.full_name}"


class CourseGroupMeetingInfo(typing.NamedTuple):
    meeting_type: MeetingType
    teachers: typing.Set[Teacher]
    # Location
    building: typing.Optional[str]
    room: typing.Optional[str]
    # Time
    semester: Semester
    day: typing.Optional[Day]
    starting_time: typing.Optional[str]
    ending_time: typing.Optional[str]


class CourseGroupInfo(typing.NamedTuple):
    course_code: str
    course_name: str
    course_group_name: str
    faculty: str
    school: str
    meetings: typing.Tuple[CourseGroupMeetingInfo, ...]

    @property
    def semester(self) -> Semester:
        semesters: typing.Set[Semester] = {meeting.semester for meeting in self.meetings}
        if len(semesters) == 1:
            return tuple(semesters)[0]
        if Semester.summer in semesters:
            _logger.error(
                "Did not expect %s-%s to have %s meetings when there are other semesters in the group as well.",
                self.course_code,
                self.course_group_name,
                Semester.summer.name,
            )
            raise ValueError(
                F"Did not expect {self.course_code}-{self.course_group_name} to have {Semester.summer.name} meetings "
                "when there are other semesters in the group as well.",
            )
        if Semester.all_year in semesters:
            _logger.error(
                "Found semester type %s in %s-%s meetings, which should only be deduced on the entire group.",
                Semester.all_year.name,
                self.course_code,
                self.course_group_name,
            )
            raise ValueError(
                F"Found semester type {Semester.all_year.name} in {self.course_code}-{self.course_group_name} "
                "meetings, which should only be deduced on the entire group.",
            )
        return Semester.all_year

    @property
    def teachers(self) -> typing.Iterable[Teacher]:
        teachers: typing.Set[Teacher] = set()
        for meeting in self.meetings:
            teachers = teachers.union(meeting.teachers)
        return teachers


class CourseInfo(typing.NamedTuple):
    course_code: str
    year: int
    course_groups: typing.List[CourseGroupInfo]
