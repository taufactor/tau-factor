from django import shortcuts as django_shortcuts
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework import decorators as drf_decorators
from rest_framework.response import Response


from courses import models as courses_models
from grades import filters as grades_filters
from grades import models as grades_models
from grades import non_persistent_models as grades_non_persistent_models
from grades import request_serializers as grades_request_serializers
from grades import serializers as grades_serializers
from grades import services as grades_services


class ExamView(viewsets.ReadOnlyModelViewSet):
    queryset = grades_models.Exam.objects.all()
    serializer_class = grades_serializers.ExamSerializer
    filterset_class = grades_filters.ExamFilters

    @swagger_auto_schema(operation_summary="List Exams", operation_description="List grade distribution of exams.")
    def list(self, request, *args, **kwargs) -> Response:
        return super(ExamView, self).list(request)

    @swagger_auto_schema(operation_summary="Retrieve Exam", operation_description="Retrieve grade distribution of an exam.")
    def retrieve(self, request, *args, **kwargs) -> Response:
        return super(ExamView, self).retrieve(request)

    @drf_decorators.action(
        detail=False,
        methods=["POST"],
        serializer_class=grades_request_serializers.ExamCreateSerializer,
    )
    @swagger_auto_schema(
        operation_summary="Create Exam",
        operation_description="Each exam is related to a specific course group and to a specific date (\"moed\").",
        responses={
            status.HTTP_201_CREATED: grades_serializers.ExamSerializer,
        },
    )
    def add_exam(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        course_group = django_shortcuts.get_object_or_404(
            klass=courses_models.CourseGroup,
            **{
                courses_models.CourseGroup.course_group_id.field.name:
                    validated_data[grades_models.Exam.course_group_id.field.attname],
            },
        )

        grade_ranges = tuple(
            grades_non_persistent_models.CreateGradeRangeParams(**grade_range_dict)
            for grade_range_dict in validated_data[grades_models.Exam.EXAM_GRADES_RELATED_FIELD_NAME]
        )

        validated_statistics = validated_data.get(grades_models.Exam.EXAM_STATISTICS_RELATED_FIELD_NAME, {})

        params = grades_non_persistent_models.CreateExamParams(
            course_group=course_group,
            moed=validated_data[grades_models.Exam.moed.field.name],
            students_count=validated_data[grades_models.Exam.students_count.field.name],
            failures_count=validated_data[grades_models.Exam.failures_count.field.name],
            mean=validated_statistics.get(grades_models.ExamStatistics.mean.field.name),
            median=validated_statistics.get(grades_models.ExamStatistics.median.field.name),
            standard_deviation=validated_statistics.get(grades_models.ExamStatistics.standard_deviation.field.name),
            grade_ranges=grade_ranges,
        )

        instance = grades_services.ExamService.get_or_create(params)
        response_serializer = grades_serializers.ExamSerializer(instance=instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
