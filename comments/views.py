from django import shortcuts as django_shortcuts
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework import decorators as drf_decorators
from rest_framework.response import Response

from comments import filters as comments_filters
from comments import models as comments_models
from comments import non_persistent_models as comments_non_persistent_models
from comments import serializers as comments_serializers
from comments import services as comments_services
from comments import request_serializers as comments_request_serializers
from courses import models as courses_models


class CourseCommentsView(viewsets.ReadOnlyModelViewSet):
    queryset = comments_models.CourseComment.objects.all()
    serializer_class = comments_serializers.CourseCommentSerializer
    filterset_class = comments_filters.CourseCommentsFilters

    @swagger_auto_schema(operation_summary="List Comments", operation_description="List comments of users on courses.")
    def list(self, request, *args, **kwargs) -> Response:
        return super(CourseCommentsView, self).list(request)

    @swagger_auto_schema(operation_summary="Retrieve Comment", operation_description="Retrieve a comment on a course.")
    def retrieve(self, request, *args, **kwargs) -> Response:
        return super(CourseCommentsView, self).retrieve(request)


class CourseCommentsPrivateView(viewsets.GenericViewSet):
    serializer_class = comments_serializers.CourseCommentSerializer

    @drf_decorators.action(
        detail=False,
        methods=["POST"],
        serializer_class=comments_request_serializers.CourseCommentCreateSerializer,
    )
    @swagger_auto_schema(
        operation_summary="Add Comment",
        operation_description="Add a comment to a course.",
        responses={
            status.HTTP_201_CREATED: comments_serializers.CourseCommentSerializer,
        },
    )
    def add_comment(self, request, *args, **kwargs) -> Response:
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        course_id = validated_data[courses_models.Course.course_id.field.attname]
        course = django_shortcuts.get_object_or_404(
            klass=courses_models.Course,
            **{
                courses_models.Course.course_id.field.name: course_id,
            },
        )

        params = comments_non_persistent_models.CreateCourseCommentParams(
            course=course,
            title=validated_data[comments_models.CourseComment.title.field.name],
            content=validated_data.get(comments_models.CourseComment.content.field.name, ""),
        )

        instance = comments_services.CourseCommentService.create(params)
        response_serializer = comments_serializers.CourseCommentSerializer(instance=instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
