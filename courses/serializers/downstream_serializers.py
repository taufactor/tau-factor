import typing

from drf_yasg.utils import swagger_serializer_method
from rest_framework import fields
from rest_framework import serializers

from courses import defines as courses_defines
from courses import models as courses_models
from courses.serializers import common_serializers as courses_common_serializers
from grades import models as grades_models
from grades import serializers as grades_serializers


class CourseGroupDownstreamSerializer(courses_common_serializers.BaseCourseGroupSerializer):
    num_exams = fields.IntegerField(required=True)

    class Meta(courses_common_serializers.BaseCourseGroupSerializer.Meta):
        fields = courses_common_serializers.BaseCourseGroupSerializer.Meta.fields + (
            courses_models.CourseGroup.NUM_EXAMS_ANNOTATION,
        )


class CourseInstanceDownstreamSerializer(courses_common_serializers.BaseCourseInstanceSerializer):
    groups = CourseGroupDownstreamSerializer(many=True)
    num_groups = fields.IntegerField()
    statistics = serializers.SerializerMethodField()

    @swagger_serializer_method(grades_serializers.ExamStatisticsSerializer(allow_null=True))
    def get_statistics(
            self,
            instance: courses_models.CourseInstance,
    ) -> typing.Optional[typing.Dict[str, typing.Any]]:
        statistics = grades_models.ExamStatistics.objects.filter(**{
            "__".join((
                grades_models.ExamStatistics.exam.field.name,
                grades_models.Exam.course_group.field.name,
                courses_models.CourseGroup.course_instance.field.name,
            )): instance,
            "__".join((
                grades_models.ExamStatistics.exam.field.name,
                grades_models.Exam.course_group.field.name,
                courses_models.CourseGroup.course_group_name.field.name,
            )): courses_defines.COURSE_GROUP_ALL_NAME,
            "__".join((
                grades_models.ExamStatistics.exam.field.name,
                grades_models.Exam.moed.field.name,
            )): 0,  # final grades
        }).first()
        return grades_serializers.ExamStatisticsSerializer(instance=statistics).data if statistics else None

    class Meta(courses_common_serializers.BaseCourseInstanceSerializer.Meta):
        fields = courses_common_serializers.BaseCourseInstanceSerializer.Meta.fields + (
            courses_models.CourseInstance.COURSE_GROUPS_RELATED_FIELD_NAME,
            courses_models.CourseInstance.NUM_GROUPS_ANNOTATION,
            "statistics",
        )


class CourseDownstreamSerializer(courses_common_serializers.BaseCourseSerializer):
    instances = CourseInstanceDownstreamSerializer(many=True)

    class Meta(courses_common_serializers.BaseCourseSerializer.Meta):
        fields = courses_common_serializers.BaseCourseSerializer.Meta.fields + (
            courses_models.Course.COURSE_INSTANCES_RELATED_FIELD_NAME,
        )
