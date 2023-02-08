import functools
import typing

from enumchoicefield import ChoiceEnum


class Language(ChoiceEnum):
    EN = "English"
    HE = "Hebrew"

    @classmethod
    def all(cls) -> typing.Tuple["Language", ...]:
        return tuple(language for language in cls)


@functools.total_ordering
class Semester(ChoiceEnum):
    A = "Semester A"
    B = "Semester B"
    SUMMER = "Summer Semester"
    ALL_YEAR = "All Year"

    def __lt__(self, other: "Semester") -> bool:
        rankings = {
            Semester.A: 0,
            Semester.B: 1,
            Semester.SUMMER: 2,
            Semester.ALL_YEAR: 3,
        }
        return rankings[self] < rankings[other]
