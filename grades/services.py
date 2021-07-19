import collections
import functools
import typing

from django.db import models as django_db_models
from django.db import transaction as django_db_transaction

from courses import models as courses_models
from courses import services as courses_services
from grades import models as grades_models
from grades import non_persistent_models as grades_non_persistent_models


class ExamService(object):
    model = grades_models.Exam

    @classmethod
    @django_db_transaction.atomic
    def get_or_create(
            cls,
            params: grades_non_persistent_models.CreateExamParams,
    ) -> grades_models.Exam:
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

        cls.recalculate_exam_for_course_group_all(params.course_group.course_instance)
        return exam

    @classmethod
    def recalculate_exam_for_course_group_all(
            cls,
            course_instance: courses_models.CourseInstance,
    ) -> None:
        with django_db_transaction.atomic():
            course_group_all = courses_services.CourseInstanceService.get_group_all(course_instance)

            # Remove old exams for the "all group" of this course instance
            grades_models.Exam.objects.filter(**{
                grades_models.Exam.course_group.field.name: course_group_all,
            }).delete()

            # Get all exams for this course instance
            exams_qs = cls.model.objects.filter(**{
                "__".join((
                    grades_models.Exam.course_group.field.name,
                    courses_models.CourseGroup.course_instance.field.name,
                )): course_instance,
            })

            moed_to_exams_mapping = collections.defaultdict(list)
            for exam in exams_qs:
                moed_to_exams_mapping[exam.moed].append(exam)

            # Recreate the exams for group all
            for moed, exams in moed_to_exams_mapping.items():
                total_students_count = functools.reduce(lambda cur, e: cur + e.students_count, exams, 0)
                total_failures_count = functools.reduce(lambda cur, e: cur + e.failures_count, exams, 0)
                new_exam = cls.model.objects.create(**{
                    grades_models.Exam.course_group.field.name: course_group_all,
                    grades_models.Exam.moed.field.name: moed,
                    grades_models.Exam.students_count.field.name: total_students_count,
                    grades_models.Exam.failures_count.field.name: total_failures_count,
                })

                # Create statistics for the new exam
                total_mean = functools.reduce(
                    lambda cur, e: cur + e.statistics.mean * e.students_count,
                    exams,
                    0,
                ) / total_students_count if total_students_count > 0 else None
                grades_models.ExamStatistics.objects.create(**{
                    grades_models.ExamStatistics.exam.field.name: new_exam,
                    grades_models.ExamStatistics.mean.field.name: total_mean,
                })

                # Create grade ranges for the new exam
                total_students_in_range_annotation = "total_students_in_range"
                grade_ranges = grades_models.ExamGradeRange.objects.filter(**{
                    "__".join((
                        grades_models.ExamGradeRange.exam.field.name,
                        grades_models.Exam.course_group.field.name,
                        courses_models.CourseGroup.course_instance.field.name,
                    )): course_instance,
                    "__".join((
                        grades_models.ExamGradeRange.exam.field.name,
                        grades_models.Exam.moed.field.name,
                    )): moed,
                }).values(
                    grades_models.ExamGradeRange.lowest_grade.field.name,
                    grades_models.ExamGradeRange.highest_grade.field.name,
                ).annotate(**{
                    total_students_in_range_annotation: django_db_models.Sum(
                        grades_models.ExamGradeRange.students_in_range.field.name,
                    )},
                )

                new_grade_ranges = []
                for grade_range in grade_ranges:
                    new_grade_ranges.append(
                        grades_models.ExamGradeRange(**{
                            grades_models.ExamGradeRange.exam.field.name:
                                new_exam,
                            grades_models.ExamGradeRange.lowest_grade.field.name:
                                grade_range[grades_models.ExamGradeRange.lowest_grade.field.name],
                            grades_models.ExamGradeRange.highest_grade.field.name:
                                grade_range[grades_models.ExamGradeRange.highest_grade.field.name],
                            grades_models.ExamGradeRange.students_in_range.field.name:
                                grade_range[total_students_in_range_annotation],
                        }),
                    )
                grades_models.ExamGradeRange.objects.bulk_create(new_grade_ranges)
