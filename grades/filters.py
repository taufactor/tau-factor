import django_filters
from django.db.models import lookups as django_db_lookups

from courses import defines as courses_defines
from courses import models as courses_models
from grades import models as grades_models


class ExamFilters(django_filters.FilterSet):
    course_id = django_filters.UUIDFilter(
        field_name="__".join((
            grades_models.Exam.course_group.field.name,
            courses_models.CourseGroup.course_instance.field.name,
            courses_models.CourseInstance.course_id.field.attname,
        )),
        distinct=True,
    )

    course_code = django_filters.CharFilter(
        field_name="__".join((
            grades_models.Exam.course_group.field.name,
            courses_models.CourseGroup.course_instance.field.name,
            courses_models.CourseInstance.course.field.name,
            courses_models.Course.course_code.field.name,
        )),
        lookup_expr=django_db_lookups.Exact.lookup_name,
        distinct=True,
        min_length=courses_defines.COURSE_CODE_LENGTH,
        max_length=courses_defines.COURSE_CODE_LENGTH,
    )

    course_group_id = django_filters.UUIDFilter()

    course_instance_id = django_filters.UUIDFilter(
        field_name="__".join((
            grades_models.Exam.course_group.field.name,
            courses_models.CourseGroup.course_instance_id.field.attname,
        )),
    )

    moed = django_filters.NumberFilter()
