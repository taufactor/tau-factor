import uuid

from django.db import models as django_db_models

from courses import models as courses_models


class Exam(django_db_models.Model):
    EXAM_STATISTICS_RELATED_FIELD_NAME = "statistics"
    EXAM_GRADES_RELATED_FIELD_NAME = "grades"

    exam_id = django_db_models.UUIDField(primary_key=True, default=uuid.uuid4)

    # Unique together
    course_group = django_db_models.ForeignKey(
        courses_models.CourseGroup,
        on_delete=django_db_models.CASCADE,
        related_name=courses_models.CourseGroup.EXAMS_RELATED_FIELD_NAME,
    )
    moed = django_db_models.PositiveSmallIntegerField(null=False)  # moed=0 is used for the final grades of all students

    students_count = django_db_models.PositiveSmallIntegerField(null=False)
    failures_count = django_db_models.PositiveSmallIntegerField(null=False)

    class Meta:
        unique_together = ("course_group", "moed")
        ordering = ("course_group", "moed")

    def __repr__(self):
        return f"{repr(self.course_group)}, Moed {self.moed}"

    def __str__(self):
        return f"Exam({repr(self)})"


class ExamStatistics(django_db_models.Model):
    exam_statistics_id = django_db_models.UUIDField(primary_key=True, default=uuid.uuid4)

    exam = django_db_models.OneToOneField(
        Exam,
        unique=True,
        on_delete=django_db_models.CASCADE,
        related_name=Exam.EXAM_STATISTICS_RELATED_FIELD_NAME,
    )

    mean = django_db_models.FloatField(blank=True, null=True)
    median = django_db_models.FloatField(blank=True, null=True)
    standard_deviation = django_db_models.FloatField(blank=True, null=True)

    def __repr__(self):
        return f"{repr(self.exam)}, Mean {self.mean}, Median{self.median}, Standard Deviation {self.standard_deviation}"

    def __str__(self):
        return f"ExamStatistics({repr(self)})"


class ExamGradeRange(django_db_models.Model):
    exam_grade_range_id = django_db_models.UUIDField(primary_key=True, default=uuid.uuid4)

    exam = django_db_models.ForeignKey(
        Exam,
        on_delete=django_db_models.CASCADE,
        related_name=Exam.EXAM_GRADES_RELATED_FIELD_NAME,
    )

    lowest_grade = django_db_models.PositiveSmallIntegerField(null=False)
    highest_grade = django_db_models.PositiveSmallIntegerField(null=False)
    students_in_range = django_db_models.PositiveSmallIntegerField(null=False)

    class Meta:
        unique_together = ("exam", "lowest_grade")
        ordering = ("lowest_grade",)

    def __repr__(self):
        suffix = "student" if self.students_in_range == 1 else "students"
        return f"{repr(self.exam)}, Grades {self.lowest_grade}-{self.highest_grade}: {self.students_in_range} {suffix}"

    def __str__(self):
        return f"ExamGradeRange({repr(self)})"
