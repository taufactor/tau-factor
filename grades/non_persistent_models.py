import typing

from courses import models as courses_models


class CreateGradeRangeParams(typing.NamedTuple):
    lowest_grade: int
    highest_grade: int
    students_in_range: int


class CreateExamParams(typing.NamedTuple):
    course_group: courses_models.CourseGroup
    moed: int
    students_count: int
    failures_count: int
    mean: typing.Optional[float]
    median: typing.Optional[float]
    standard_deviation: typing.Optional[float]
    grade_ranges: typing.Sequence[CreateGradeRangeParams]
