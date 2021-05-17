import django_filters
from django.db.models import lookups as django_db_lookups

from courses import defines as courses_defines
from courses import models as courses_models
from ratings import models as ratings_models


class RatingsFilters(django_filters.FilterSet):
    course_id = django_filters.UUIDFilter()

    course_code = django_filters.CharFilter(
        field_name="__".join((
            ratings_models.CourseRating.course.field.name,
            courses_models.Course.course_code.field.name,
        )),
        lookup_expr=django_db_lookups.Exact.lookup_name,
        distinct=True,
        min_length=courses_defines.COURSE_CODE_LENGTH,
        max_length=courses_defines.COURSE_CODE_LENGTH,
    )
