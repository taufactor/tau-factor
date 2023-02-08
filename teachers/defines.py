import functools
import typing

from enumchoicefield import ChoiceEnum

from common import defines as common_defines

TEACHER_NAME_MAX_LENGTH = 255


@functools.total_ordering
class Honorific(ChoiceEnum):
    MR = "Mr."
    MS = "Ms."
    DR = "Dr."
    PROF = "Prof."

    @classmethod
    def all(cls) -> typing.Tuple["Honorific", ...]:
        return tuple(honorific for honorific in cls)

    def to_string(self, language: common_defines.Language) -> str:
        language_to_honorific_string_mappings = {
            common_defines.Language.EN: {honorific: honorific.value for honorific in Honorific.all()},
            common_defines.Language.HE: {
                Honorific.MR: "מר",
                Honorific.MS: "גב'",
                Honorific.DR: "ד\"ר",
                Honorific.PROF: "פרופ'",
            },
        }
        return language_to_honorific_string_mappings[language][self]

    def __lt__(self, other: "Honorific") -> bool:
        rankings = {
            Honorific.MR: 0,
            Honorific.MS: 0,
            Honorific.DR: 1,
            Honorific.PROF: 2,
        }
        return rankings[self] < rankings[other]
