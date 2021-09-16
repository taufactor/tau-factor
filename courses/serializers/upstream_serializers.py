from courses import models as courses_models
from courses.serializers import common_serializers as courses_common_serializers


class CourseUpstreamSerializer(courses_common_serializers.BaseCourseSerializer):
    class Meta(courses_common_serializers.BaseCourseSerializer.Meta):
        pass


class CourseInstanceUpstreamSerializer(courses_common_serializers.BaseCourseInstanceSerializer):
    course = CourseUpstreamSerializer()

    class Meta(courses_common_serializers.BaseCourseInstanceSerializer.Meta):
        fields = courses_common_serializers.BaseCourseInstanceSerializer.Meta.fields + (
            courses_models.CourseInstance.course.field.name,
        )


class CourseGroupUpstreamSerializer(courses_common_serializers.BaseCourseGroupSerializer):
    course_instance = CourseInstanceUpstreamSerializer()

    class Meta(courses_common_serializers.BaseCourseGroupSerializer.Meta):
        fields = courses_common_serializers.BaseCourseGroupSerializer.Meta.fields + (
            courses_models.CourseGroup.course_instance.field.name,
        )
