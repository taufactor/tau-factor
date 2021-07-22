from django import shortcuts as django_shortcuts
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework import decorators as drf_decorators
from rest_framework.response import Response

from courses import models as courses_models
from ratings import defines as ratings_defines
from ratings import filters as ratings_filters
from ratings import models as ratings_models
from ratings import request_serializers as ratings_request_serializers
from ratings import serializers as ratings_serializers
from ratings import services as ratings_services


class CourseRatingsView(viewsets.ReadOnlyModelViewSet):
    queryset = ratings_models.CourseRating.objects.all()
    serializer_class = ratings_serializers.CourseRatingSerializer
    filterset_class = ratings_filters.RatingsFilters

    @swagger_auto_schema(operation_summary="List Ratings", operation_description="List user ratings of courses.")
    def list(self, request, *args, **kwargs) -> Response:
        return super(CourseRatingsView, self).list(request)

    @swagger_auto_schema(operation_summary="Retrieve Rating", operation_description="Retrieve the rating of a course.")
    def retrieve(self, request, *args, **kwargs) -> Response:
        return super(CourseRatingsView, self).retrieve(request)


class CourseRatingsPrivateView(viewsets.GenericViewSet):
    serializer_class = ratings_serializers.CourseRatingSerializer

    @drf_decorators.action(
        detail=False,
        methods=["POST"],
        serializer_class=ratings_request_serializers.CourseRatingVoteSerializer,
    )
    @swagger_auto_schema(
        operation_summary="Rate Course",
        operation_description="Rate a course.",
        responses={
            status.HTTP_200_OK: ratings_serializers.CourseRatingSerializer,
        },
    )
    def vote(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        course_id = validated_data[courses_models.Course.course_id.field.attname]
        rating = validated_data["rating"]

        course = django_shortcuts.get_object_or_404(
            klass=courses_models.Course,
            **{
                courses_models.Course.course_id.field.name: course_id,
            },
        )

        user_votes_session = request.session.get(ratings_defines.USER_VOTING_SESSION_NAME, [])

        service = ratings_services.CourseRatingService
        if str(course_id) in user_votes_session:
            instance = service.get_object(course=course)
        else:
            instance = service.vote(course=course, rating=rating)
            user_votes_session.append(str(course_id))
            request.session[ratings_defines.USER_VOTING_SESSION_NAME] = user_votes_session

        response_serializer = ratings_serializers.CourseRatingSerializer(
            instance=instance,
            context=self.get_serializer_context(),
        )
        return Response(response_serializer.data, status=status.HTTP_200_OK)
