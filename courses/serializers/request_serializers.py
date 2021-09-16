import re

from django.core import validators as django_validators
from rest_framework import fields
from rest_framework import serializers

from courses import defines as courses_defines
from courses import models as courses_models


class CourseInstanceNameCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = courses_models.CourseInstanceName
        fields = (
            courses_models.CourseInstanceName.language.field.name,
            courses_models.CourseInstanceName.course_name.field.name,
        )


class CourseInstanceCreateSerializer(serializers.ModelSerializer):
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
    names = CourseInstanceNameCreateSerializer(many=True, required=True)

    class Meta:
        model = courses_models.CourseInstance
        fields = (
            courses_models.Course.course_code.field.name,
            courses_models.CourseInstance.year.field.name,
            courses_models.CourseInstance.semester.field.name,
            courses_models.CourseInstance.COURSE_NAMES_RELATED_FIELD_NAME,
        )


class CourseGroupTeacherCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = courses_models.CourseGroupTeacher
        fields = (
            courses_models.CourseGroupTeacher.teacher_name.field.name,
        )


class CourseGroupCreateSerializer(serializers.ModelSerializer):
    course_instance_id = fields.UUIDField(required=True)
    teachers = CourseGroupTeacherCreateSerializer(many=True, required=False)

    class Meta:
        model = courses_models.CourseGroup
        fields = (
            courses_models.CourseGroup.course_instance_id.field.attname,
            courses_models.CourseGroup.course_group_name.field.name,
            courses_models.CourseGroup.TEACHERS_RELATED_FIELD_NAME,
        )
