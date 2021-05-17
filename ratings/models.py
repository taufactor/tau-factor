import typing
import uuid

from django.db import models as django_db_models

from courses import models as courses_models
from ratings import defines as ratings_defines


class CourseRating(django_db_models.Model):
    RATING_PROPERTY_NAME = "rating"

    course_rating_id = django_db_models.UUIDField(primary_key=True, default=uuid.uuid4)

    course = django_db_models.OneToOneField(
        courses_models.Course,
        unique=True,
        on_delete=django_db_models.CASCADE,
        related_name=courses_models.Course.COURSE_RATING_RELATED_FIELD_NAME,
    )

    # If we start supporting logins, then we should manage a Votings model
    total_votes = django_db_models.PositiveIntegerField(default=0)
    summed_votes = django_db_models.PositiveIntegerField(default=0)

    @property
    def rating(self) -> typing.Optional[float]:
        return round(
            self.summed_votes / self.total_votes,
            ratings_defines.RATING_NUM_DECIMALS,
        ) if self.total_votes > 0 else None

    def __repr__(self):
        return f"{repr(self.course)}, {self.rating} ({self.summed_votes}/{self.total_votes})"

    def __str__(self):
        return f"CourseRating({repr(self)})"
