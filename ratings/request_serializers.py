import re

from django.core import validators as django_validators
from rest_framework import serializers
from rest_framework import fields

from courses import defines as courses_defines
from courses import models as courses_models
from ratings import defines as ratings_defines
from ratings import models as ratings_models


class CourseRatingVoteSerializer(serializers.Serializer):
    course_id = fields.UUIDField(required=True)
    rating = fields.IntegerField(
        min_value=ratings_defines.MIN_VOTE_VALUE,
        max_value=ratings_defines.MAX_VOTE_VALUE,
        required=True,
    )


class CourseRatingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ratings_models.CourseRating
        fields = (
            ratings_models.CourseRating.total_votes.field.name,
            ratings_models.CourseRating.summed_votes.field.name,
        )


class CourseRatingUpdateSerializer(serializers.ModelSerializer):
    course_code = fields.CharField(
        required=True,
        max_length=courses_defines.COURSE_CODE_LENGTH,
        validators=(
            django_validators.RegexValidator(
                regex=re.compile(r"^\d{4}-\d{4}$"),
                message=courses_defines.COURSE_CODE_VALIDATION_ERROR,
            ),
        ),
    )

    class Meta:
        model = ratings_models.CourseRating
        fields = (
            courses_models.Course.course_code.field.name,
            ratings_models.CourseRating.total_votes.field.name,
            ratings_models.CourseRating.summed_votes.field.name,
        )
