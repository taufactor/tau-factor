import typing

from courses import models as courses_models


class CreateCourseCommentParams(typing.NamedTuple):
    course: courses_models.Course
    title: str
    content: str
