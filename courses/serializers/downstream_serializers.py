from rest_framework import fields

from courses import models as courses_models
from courses.serializers import common_serializers as courses_common_serializers


class CourseGroupDownstreamSerializer(courses_common_serializers.BaseCourseGroupSerializer):
    num_exams = fields.IntegerField(required=True)

    class Meta(courses_common_serializers.BaseCourseGroupSerializer.Meta):
        fields = courses_common_serializers.BaseCourseGroupSerializer.Meta.fields + (
            courses_models.CourseGroup.NUM_EXAMS_ANNOTATION,
        )


class CourseInstanceDownstreamSerializer(courses_common_serializers.BaseCourseInstanceSerializer):
    groups = CourseGroupDownstreamSerializer(many=True)
    num_groups = fields.IntegerField()

    class Meta(courses_common_serializers.BaseCourseInstanceSerializer.Meta):
        fields = courses_common_serializers.BaseCourseInstanceSerializer.Meta.fields + (
            courses_models.CourseInstance.COURSE_GROUPS_RELATED_FIELD_NAME,
            courses_models.CourseInstance.NUM_GROUPS_ANNOTATION,
        )


class CourseDownstreamSerializer(courses_common_serializers.BaseCourseSerializer):
    instances = CourseInstanceDownstreamSerializer(many=True)

    class Meta(courses_common_serializers.BaseCourseSerializer.Meta):
        fields = courses_common_serializers.BaseCourseSerializer.Meta.fields + (
            courses_models.Course.COURSE_INSTANCES_RELATED_FIELD_NAME,
        )
