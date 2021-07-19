from enumchoicefield import ChoiceEnum

COURSE_CODE_LENGTH = len("xxxx-xxxx")
COURSE_CODE_VALIDATION_ERROR = "Course code format must be xxxx-xxxx"

COURSE_NAME_MAX_LENGTH = 255
TEACHER_NAME_MAX_LENGTH = 255

COURSE_GROUP_ALL_NAME = "00"


class Semester(ChoiceEnum):
    A = "Semester A"
    B = "Semester B"
    SUMMER = "Summer Semester"
    ALL_YEAR = "All Year"


class Language(ChoiceEnum):
    EN = "English"
    HE = "Hebrew"
