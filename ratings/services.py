from django import shortcuts as django_shortcuts
from django.db import models as django_db_models

from courses import models as courses_models
from ratings import models as ratings_models


class CourseRatingService(object):
    model = ratings_models.CourseRating

    @classmethod
    def get_or_create(
            cls,
            course: courses_models.Course,
    ) -> courses_models.Course:
        course_rating, _ = cls.model.objects.get_or_create(
            defaults={},
            **{
                ratings_models.CourseRating.course.field.name: course,
            },
        )
        return course_rating

    @classmethod
    def get_object(cls, course: courses_models.Course) -> ratings_models.CourseRating:
        return django_shortcuts.get_object_or_404(
            klass=cls.model,
            **{
                ratings_models.CourseRating.course.field.name: course,
            },
        )

    @classmethod
    def vote(cls, course: courses_models.Course, rating: int) -> ratings_models.CourseRating:
        course_rating = cls.get_object(course)

        course_rating.total_votes = django_db_models.F(ratings_models.CourseRating.total_votes.field.name) + 1
        course_rating.summed_votes = django_db_models.F(ratings_models.CourseRating.summed_votes.field.name) + rating
        course_rating.save(
            update_fields=(
                ratings_models.CourseRating.total_votes.field.name,
                ratings_models.CourseRating.summed_votes.field.name,
            ),
        )

        course_rating.refresh_from_db()
        return course_rating
