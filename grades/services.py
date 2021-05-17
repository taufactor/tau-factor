from django.db import transaction as django_db_transaction

from courses import models as courses_models
from grades import models as grades_models
from grades import non_persistent_models as grades_non_persistent_models


class ExamService(object):
    model = grades_models.Exam

    @classmethod
    @django_db_transaction.atomic
    def get_or_create(
            cls,
            params: grades_non_persistent_models.CreateExamParams,
    ) -> courses_models.CourseInstance:
        exam, _ = cls.model.objects.get_or_create(
            defaults={},
            **{
                grades_models.Exam.course_group.field.name: params.course_group,
                grades_models.Exam.moed.field.name: params.moed,
                grades_models.Exam.students_count.field.name: params.students_count,
                grades_models.Exam.failures_count.field.name: params.failures_count,
            }
        )

        grades_models.ExamStatistics.objects.get_or_create(
            defaults={
                grades_models.ExamStatistics.mean.field.name: params.mean,
                grades_models.ExamStatistics.median.field.name: params.median,
                grades_models.ExamStatistics.standard_deviation.field.name: params.standard_deviation,
            },
            **{
                grades_models.ExamStatistics.exam.field.name: exam,
            },
        )

        grade_ranges = tuple(
            grades_models.ExamGradeRange(**{
                grades_models.ExamGradeRange.exam.field.name: exam,
                grades_models.ExamGradeRange.lowest_grade.field.name: grade_range_params.lowest_grade,
                grades_models.ExamGradeRange.highest_grade.field.name: grade_range_params.highest_grade,
                grades_models.ExamGradeRange.students_in_range.field.name: grade_range_params.students_in_range,
            })
            for grade_range_params in params.grade_ranges
        )
        grades_models.ExamGradeRange.objects.bulk_create(grade_ranges, ignore_conflicts=True)

        return exam
