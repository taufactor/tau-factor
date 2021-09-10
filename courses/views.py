from django import http as django_http
from django import shortcuts as django_shortcuts
from django.db import models as django_db_models
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework import decorators as drf_decorators
from rest_framework.request import Request
from rest_framework.response import Response


from courses import exceptions as courses_exceptions
from courses import filters as courses_filters
from courses import models as courses_models
from courses import non_persistent_models as courses_non_persistent_models
from courses import request_serializers as courses_request_serializers
from courses import serializers as courses_serializers
from courses import services as courses_services
from grades import services as grades_services
from grades import serializers as grades_serializers


class CoursesView(viewsets.ReadOnlyModelViewSet):
    serializer_class = courses_serializers.CourseSerializer
    filterset_class = courses_filters.CoursesFilters

    def get_queryset(self) -> django_db_models.QuerySet:
        return courses_models.Course.objects.all().prefetch_related(
            django_db_models.Prefetch(
                lookup="__".join((
                    courses_models.Course.COURSE_INSTANCES_RELATED_FIELD_NAME,
                    courses_models.CourseInstance.COURSE_NAMES_RELATED_FIELD_NAME,
                )),
                queryset=courses_models.CourseInstanceName.objects.order_by(
                    courses_models.CourseInstanceName.course_name.field.name,
                )
            ),
            django_db_models.Prefetch(
                lookup="__".join((
                    courses_models.Course.COURSE_INSTANCES_RELATED_FIELD_NAME,
                    courses_models.CourseInstance.COURSE_GROUPS_RELATED_FIELD_NAME,
                )),
                queryset=courses_models.CourseGroup.objects.order_by(
                    courses_models.CourseGroup.course_group_name.field.name,
                )
            ),
            django_db_models.Prefetch(
                lookup="__".join((
                    courses_models.Course.COURSE_INSTANCES_RELATED_FIELD_NAME,
                    courses_models.CourseInstance.COURSE_GROUPS_RELATED_FIELD_NAME,
                    courses_models.CourseGroup.TEACHERS_RELATED_FIELD_NAME,
                )),
                queryset=courses_models.CourseGroupTeacher.objects.order_by(
                    courses_models.CourseGroupTeacher.teacher_name.field.name,
                )
            ),
        )

    @swagger_auto_schema(operation_summary="List Courses", operation_description="List courses.")
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super(CoursesView, self).list(request)

    @swagger_auto_schema(operation_summary="Retrieve Course", operation_description="Retrieve a course.")
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        return super(CoursesView, self).retrieve(request)

    @drf_decorators.action(
        detail=True,
        methods=["GET"],
        serializer_class=grades_serializers.ExamSerializer,
    )
    @swagger_auto_schema(
        operation_summary="Get Latest Exam",
        operation_description="Get most recent exam of the course.",
    )
    def latest_exam(self, request, *args, **kwargs) -> Response:
        course = self.get_object()
        exam = grades_services.ExamService.get_latest_exam_for_course(course=course)
        if exam is None:
            raise django_http.Http404
        return Response(grades_serializers.ExamSerializer(exam).data)


class CoursesInstanceView(viewsets.GenericViewSet):
    serializer_class = courses_serializers.CourseInstanceSerializer

    @drf_decorators.action(
        detail=False,
        methods=["POST"],
        serializer_class=courses_request_serializers.CourseInstanceCreateSerializer,
    )
    @swagger_auto_schema(
        operation_summary="Create Course Instance",
        operation_description="Each course instance represents a specific ```course code```, ```year``` and ```semester```.",
        responses={
            status.HTTP_201_CREATED: courses_serializers.CourseInstanceSerializer,
        },
    )
    def create_course(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        course_instance_names = {
            course_name_dict[courses_models.CourseInstanceName.language.field.name]:
                course_name_dict[courses_models.CourseInstanceName.course_name.field.name]
            for course_name_dict in validated_data[courses_models.CourseInstance.COURSE_NAMES_RELATED_FIELD_NAME]
        }

        if len(course_instance_names) != len(validated_data[courses_models.CourseInstance.COURSE_NAMES_RELATED_FIELD_NAME]):
            raise courses_exceptions.CourseNamesLanguagesNotUnique

        params = courses_non_persistent_models.CreateCourseInstanceParams(
            course_code=validated_data[courses_models.Course.course_code.field.name],
            year=validated_data[courses_models.CourseInstance.year.field.name],
            semester=validated_data[courses_models.CourseInstance.semester.field.name],
            course_instance_names=course_instance_names,
        )

        instance = courses_services.CourseInstanceService.get_or_create(params)
        response_serializer = courses_serializers.CourseInstanceSerializer(instance=instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class CoursesGroupView(viewsets.GenericViewSet):
    serializer_class = courses_serializers.CourseGroupSerializer

    @drf_decorators.action(
        detail=False,
        methods=["POST"],
        serializer_class=courses_request_serializers.CourseGroupCreateSerializer,
    )
    @swagger_auto_schema(
        operation_summary="Create Course Group",
        operation_description="A course group is related to a specific course instance. "
                              "The group name ```00``` should be used as \"determining grades\" group.",
        responses={
            status.HTTP_201_CREATED: courses_serializers.CourseGroupSerializer,
        },
    )
    def create_course_group(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        course_instance = django_shortcuts.get_object_or_404(
            klass=courses_models.CourseInstance,
            **{
                courses_models.CourseInstance.course_instance_id.field.name:
                    validated_data[courses_models.CourseGroup.course_instance_id.field.attname],
            },
        )

        teacher_names = tuple(
            group_name_dict[courses_models.CourseGroupTeacher.teacher_name.field.name]
            for group_name_dict in validated_data.get(courses_models.CourseGroup.TEACHERS_RELATED_FIELD_NAME, {})
        )

        params = courses_non_persistent_models.CreateCourseGroupParams(
            course_instance=course_instance,
            group_name=validated_data[courses_models.CourseGroup.course_group_name.field.name],
            teacher_names=teacher_names,
        )

        instance = courses_services.CourseGroupService.get_or_create(params)
        response_serializer = courses_serializers.CourseGroupSerializer(instance=instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
