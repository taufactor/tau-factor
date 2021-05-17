from rest_framework import fields
from rest_framework import serializers

from grades import models as grades_models


class ExamGradeRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = grades_models.ExamGradeRange
        fields = (
            grades_models.ExamGradeRange.lowest_grade.field.name,
            grades_models.ExamGradeRange.highest_grade.field.name,
            grades_models.ExamGradeRange.students_in_range.field.name,
        )


class ExamStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = grades_models.ExamStatistics
        fields = (
            grades_models.ExamStatistics.mean.field.name,
            grades_models.ExamStatistics.median.field.name,
            grades_models.ExamStatistics.standard_deviation.field.name,
        )


class ExamSerializer(serializers.ModelSerializer):
    course_group_id = fields.UUIDField(),
    statistics = ExamStatisticsSerializer()
    grades = ExamGradeRangeSerializer(many=True)

    class Meta:
        model = grades_models.Exam
        fields = (
            grades_models.Exam.course_group_id.field.attname,
            grades_models.Exam.moed.field.name,
            grades_models.Exam.students_count.field.name,
            grades_models.Exam.failures_count.field.name,
            grades_models.Exam.EXAM_STATISTICS_RELATED_FIELD_NAME,
            grades_models.Exam.EXAM_GRADES_RELATED_FIELD_NAME,
        )
