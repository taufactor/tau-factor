import re
import uuid

from enumchoicefield import EnumChoiceField
from django.core import validators as django_validators
from django.db import models as django_db_models

from common import defines as common_defines
from courses import defines as courses_defines


class Course(django_db_models.Model):
    MOST_COMMON_COURSE_NAMES_FIELD_NAME = "most_common_names"
    COURSE_INSTANCES_RELATED_FIELD_NAME = "instances"
    COURSE_COMMENTS_FIELD_NAME = "comments"
    COURSE_RATING_RELATED_FIELD_NAME = "rating"

    course_id = django_db_models.UUIDField(primary_key=True, default=uuid.uuid4)

    course_code = django_db_models.CharField(
        max_length=courses_defines.COURSE_CODE_LENGTH,
        null=False,
        db_index=True,
        unique=True,
        validators=(
            django_validators.RegexValidator(
                regex=re.compile(r"^\d{4}-\d{4}$"),
                message=courses_defines.COURSE_CODE_VALIDATION_ERROR,
            ),
        ),
    )

    def __repr__(self):
        return f"{self.course_code}"

    def __str__(self):
        return f"Course({repr(self)})"


class CourseInstanceManager(django_db_models.Manager):
    def get_queryset(self) -> django_db_models.QuerySet:
        qs = super(CourseInstanceManager, self).get_queryset()
        return qs.annotate(**{
            CourseInstance.NUM_GROUPS_ANNOTATION:
                django_db_models.Count(CourseInstance.COURSE_GROUPS_RELATED_FIELD_NAME),
        }).order_by(
            CourseInstance.course.field.name,
            f"-{CourseInstance.year.field.name}",
            f"-{CourseInstance.semester.field.name}",
        )


class CourseInstance(django_db_models.Model):
    COURSE_NAMES_RELATED_FIELD_NAME = "names"

    COURSE_GROUPS_RELATED_FIELD_NAME = "groups"
    NUM_GROUPS_ANNOTATION = "num_groups"

    course_instance_id = django_db_models.UUIDField(primary_key=True, default=uuid.uuid4)

    # Unique together
    course = django_db_models.ForeignKey(
        Course,
        on_delete=django_db_models.CASCADE,
        related_name=Course.COURSE_INSTANCES_RELATED_FIELD_NAME,
    )
    year = django_db_models.PositiveIntegerField(
        null=False,
        validators=(
            django_validators.MinValueValidator(2000),
            django_validators.MaxValueValidator(2040),
        ),
    )
    semester = EnumChoiceField(courses_defines.Semester, null=False)

    class Meta:
        unique_together = ("course", "year", "semester")
        ordering = ("course", "-year", "-semester")

    objects = CourseInstanceManager()

    def __repr__(self):
        return f"{repr(self.course)}, Year {self.year}, {self.semester}"

    def __str__(self):
        return f"CourseInstance({repr(self)})"


class CourseName(django_db_models.Model):
    course_name_id = django_db_models.UUIDField(primary_key=True, default=uuid.uuid4)

    language = EnumChoiceField(common_defines.Language, null=False)

    course_name = django_db_models.CharField(
        max_length=courses_defines.COURSE_NAME_MAX_LENGTH,
        null=False,
        db_index=True,
    )

    class Meta:
        abstract = True


class CourseCommonName(CourseName):
    course = django_db_models.ForeignKey(
        Course,
        on_delete=django_db_models.CASCADE,
        related_name=Course.MOST_COMMON_COURSE_NAMES_FIELD_NAME,
    )

    class Meta:
        unique_together = ("course", "language")
        # HE before EN
        ordering = ("course", "-language")

    def __repr__(self):
        return f"{repr(self.course)}, {self.course_name}"

    def __str__(self):
        return f"CourseCommonName({repr(self)})"


class CourseInstanceName(CourseName):
    course_instance = django_db_models.ForeignKey(
        CourseInstance,
        on_delete=django_db_models.CASCADE,
        related_name=CourseInstance.COURSE_NAMES_RELATED_FIELD_NAME,
    )

    class Meta:
        unique_together = ("course_instance", "language")
        # HE before EN
        ordering = ("course_instance", "-language")

    def __repr__(self):
        return f"{repr(self.course_instance)}, {self.course_name}"

    def __str__(self):
        return f"CourseInstanceName({repr(self)})"


class CourseGroupManager(django_db_models.Manager):
    def get_queryset(self) -> django_db_models.QuerySet:
        qs = super(CourseGroupManager, self).get_queryset()
        return qs.annotate(**{
            CourseGroup.NUM_EXAMS_ANNOTATION: django_db_models.Count(CourseGroup.EXAMS_RELATED_FIELD_NAME),
        })


class CourseGroup(django_db_models.Model):
    EXAMS_RELATED_FIELD_NAME = "exams"
    NUM_EXAMS_ANNOTATION = "num_exams"

    TEACHERS_RELATED_FIELD_NAME = "teachers"

    course_group_id = django_db_models.UUIDField(primary_key=True, default=uuid.uuid4)

    course_instance = django_db_models.ForeignKey(
        CourseInstance,
        on_delete=django_db_models.CASCADE,
        related_name=CourseInstance.COURSE_GROUPS_RELATED_FIELD_NAME,
    )

    course_group_name = django_db_models.CharField(max_length=4, null=False)

    class Meta:
        unique_together = ("course_instance", "course_group_name")
        ordering = ("course_instance", "course_group_name")

    objects = CourseGroupManager()

    def __repr__(self):
        return f"{repr(self.course_instance)}, Group {self.course_group_name}"

    def __str__(self):
        return f"CourseGroup({repr(self)})"


class CourseGroupTeacher(django_db_models.Model):
    teacher_id = django_db_models.UUIDField(primary_key=True, default=uuid.uuid4)

    course_group = django_db_models.ForeignKey(
        CourseGroup,
        on_delete=django_db_models.CASCADE,
        related_name=CourseGroup.TEACHERS_RELATED_FIELD_NAME,
    )

    teacher_name = django_db_models.CharField(
        max_length=courses_defines.TEACHER_NAME_MAX_LENGTH,
        null=False,
    )

    class Meta:
        unique_together = ("course_group", "teacher_name")
        ordering = ("course_group", "teacher_name")

    def __repr__(self):
        return f"{repr(self.course_group)}, Teacher {self.teacher_name}"

    def __str__(self):
        return f"CourseGroupTeacher({repr(self)})"
