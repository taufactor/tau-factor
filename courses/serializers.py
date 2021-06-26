from rest_framework import fields
from rest_framework import serializers

from courses import models as courses_models


class CourseCommonNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = courses_models.CourseCommonName
        fields = (
            courses_models.CourseCommonName.language.field.name,
            courses_models.CourseCommonName.course_name.field.name,
        )


class CourseInstanceNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = courses_models.CourseInstanceName
        fields = (
            courses_models.CourseInstanceName.language.field.name,
            courses_models.CourseInstanceName.course_name.field.name,
        )


class CourseGroupTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = courses_models.CourseGroupTeacher
        fields = (
            courses_models.CourseGroupTeacher.teacher_name.field.name,
        )


class CourseGroupSerializer(serializers.ModelSerializer):
    course_group_id = fields.UUIDField(required=True)
    teachers = CourseGroupTeacherSerializer(many=True, required=True)
    num_exams = fields.IntegerField(required=True)

    class Meta:
        model = courses_models.CourseGroup
        fields = (
            courses_models.CourseGroup.course_group_id.field.name,
            courses_models.CourseGroup.course_group_name.field.name,
            courses_models.CourseGroup.TEACHERS_RELATED_FIELD_NAME,
            courses_models.CourseGroup.NUM_EXAMS_ANNOTATION,
        )


class CourseInstanceSerializer(serializers.ModelSerializer):
    names = CourseInstanceNameSerializer(many=True)

    groups = CourseGroupSerializer(many=True)
    num_groups = fields.IntegerField()

    class Meta:
        model = courses_models.CourseInstance
        fields = (
            courses_models.CourseInstance.course_instance_id.field.name,
            courses_models.CourseInstance.year.field.name,
            courses_models.CourseInstance.semester.field.name,
            courses_models.CourseInstance.COURSE_NAMES_RELATED_FIELD_NAME,
            courses_models.CourseInstance.COURSE_GROUPS_RELATED_FIELD_NAME,
            courses_models.CourseInstance.NUM_GROUPS_ANNOTATION,
        )


class CourseSerializer(serializers.ModelSerializer):
    most_common_names = CourseCommonNameSerializer(many=True)
    instances = CourseInstanceSerializer(many=True)

    class Meta:
        model = courses_models.Course
        fields = (
            courses_models.Course.course_id.field.name,
            courses_models.Course.course_code.field.name,
            courses_models.Course.COURSE_INSTANCES_RELATED_FIELD_NAME,
            courses_models.Course.MOST_COMMON_COURSE_NAMES_FIELD_NAME,
        )
