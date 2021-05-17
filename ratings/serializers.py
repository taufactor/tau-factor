from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework import fields
from rest_framework.request import Request

from ratings import defines as ratings_defines
from ratings import models as ratings_models


class CourseRatingSerializer(serializers.ModelSerializer):
    course_id = fields.UUIDField(required=True)
    rating = fields.FloatField(required=True)
    can_vote = fields.SerializerMethodField()

    class Meta:
        model = ratings_models.CourseRating
        fields = (
            ratings_models.CourseRating.course_id.field.attname,
            ratings_models.CourseRating.RATING_PROPERTY_NAME,
            ratings_defines.CAN_VOTE_FIELD_NAME,
        )

    @swagger_serializer_method(serializer_or_field=fields.BooleanField)
    def get_can_vote(self, instance):
        request: Request = self.context["request"]
        user_votes_session = request.session.get(ratings_defines.USER_VOTING_SESSION_NAME, [])
        return str(instance.course_id) not in user_votes_session
