import django_filters
from django.db.models import lookups as django_db_lookups

from courses import defines as courses_defines
from courses import models as courses_models


class CoursesFilters(django_filters.FilterSet):
    # If both course_code and teacher filters are provided,
    # then courses answering either one will be returned (Or condition)
    # as both use related fields

    CONTAINS_FILTER_MIN_LENGTH = 3
    STARTS_WITH_FILTER_MIN_LENGTH = 3

    course_name = django_filters.CharFilter(
        field_name="__".join((
            courses_models.Course.MOST_COMMON_COURSE_NAMES_FIELD_NAME,
            courses_models.CourseCommonName.course_name.field.name,
        )),
        lookup_expr=django_db_lookups.IContains.lookup_name,
        min_length=CONTAINS_FILTER_MIN_LENGTH,
        max_length=courses_defines.COURSE_NAME_MAX_LENGTH,
    )

    course_code = django_filters.CharFilter(
        lookup_expr=django_db_lookups.StartsWith.lookup_name,
        min_length=STARTS_WITH_FILTER_MIN_LENGTH,
        max_length=courses_defines.COURSE_CODE_LENGTH,
    )

    teacher = django_filters.CharFilter(
        field_name="__".join((
            courses_models.Course.COURSE_INSTANCES_RELATED_FIELD_NAME,
            courses_models.CourseInstance.COURSE_GROUPS_RELATED_FIELD_NAME,
            courses_models.CourseGroup.TEACHERS_RELATED_FIELD_NAME,
            courses_models.CourseGroupTeacher.teacher_name.field.name,
        )),
        lookup_expr=django_db_lookups.IContains.lookup_name,
        distinct=True,
        min_length=CONTAINS_FILTER_MIN_LENGTH,
        max_length=courses_defines.TEACHER_NAME_MAX_LENGTH,
    )


class CoursesInstanceFilters(django_filters.FilterSet):
    # If both course_code and teacher filters are provided,
    # then courses answering either one will be returned (Or condition)
    # as both use related fields

    CONTAINS_FILTER_MIN_LENGTH = 3
    STARTS_WITH_FILTER_MIN_LENGTH = 3

    course_id = django_filters.UUIDFilter()

    course_name = django_filters.CharFilter(
        field_name="__".join((
            courses_models.CourseInstance.course.field.name,
            courses_models.Course.MOST_COMMON_COURSE_NAMES_FIELD_NAME,
            courses_models.CourseCommonName.course_name.field.name,
        )),
        lookup_expr=django_db_lookups.IContains.lookup_name,
        min_length=CONTAINS_FILTER_MIN_LENGTH,
        max_length=courses_defines.COURSE_NAME_MAX_LENGTH,
    )

    course_code = django_filters.CharFilter(
        field_name="__".join((
            courses_models.CourseInstance.course.field.name,
            courses_models.Course.course_code.field.name,
        )),
        lookup_expr=django_db_lookups.StartsWith.lookup_name,
        min_length=STARTS_WITH_FILTER_MIN_LENGTH,
        max_length=courses_defines.COURSE_CODE_LENGTH,
    )

    teacher = django_filters.CharFilter(
        field_name="__".join((
            courses_models.CourseInstance.COURSE_GROUPS_RELATED_FIELD_NAME,
            courses_models.CourseGroup.TEACHERS_RELATED_FIELD_NAME,
            courses_models.CourseGroupTeacher.teacher_name.field.name,
        )),
        lookup_expr=django_db_lookups.IContains.lookup_name,
        distinct=True,
        min_length=CONTAINS_FILTER_MIN_LENGTH,
        max_length=courses_defines.TEACHER_NAME_MAX_LENGTH,
    )
