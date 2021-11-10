import typing

from common import defines as common_defines
from courses import defines as courses_defines
from courses import models as courses_models


class CreateCourseInstanceParams(typing.NamedTuple):
    course_code: str
    year: int
    semester: courses_defines.Semester
    course_instance_names: typing.Dict[common_defines.Language, str]


class CreateCourseGroupParams(typing.NamedTuple):
    course_instance: courses_models.CourseInstance
    group_name: str
    teacher_names: typing.Sequence[str]
