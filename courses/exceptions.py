from rest_framework import exceptions


class CourseNamesLanguagesNotUnique(exceptions.ValidationError):
    default_detail = "Course name language must not repeat itself."
    default_code = 'course_name_language_not_unique'
