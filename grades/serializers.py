from rest_framework import fields
from rest_framework import serializers

from courses.serializers import upstream_serializers as courses_upstream_serializers
from grades import models as grades_models


class ExamGradeRangeSerializer(serializers.ModelSerializer):
    students_percent_in_range = fields.FloatField()

    class Meta:
        model = grades_models.ExamGradeRange
        fields = (
            grades_models.ExamGradeRange.lowest_grade.field.name,
            grades_models.ExamGradeRange.highest_grade.field.name,
            grades_models.ExamGradeRange.students_in_range.field.name,
            grades_models.ExamGradeRange.STUDENTS_PERCENT_IN_RANGE_PROPERTY_NAME,
        )

    def get_students_percent(self, instance):
        return instance.students_in_range / instance.exam.students_count * 100


class ExamStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = grades_models.ExamStatistics
        fields = (
            grades_models.ExamStatistics.mean.field.name,
            grades_models.ExamStatistics.median.field.name,
            grades_models.ExamStatistics.standard_deviation.field.name,
        )


class ExamSerializer(serializers.ModelSerializer):
    course_group = courses_upstream_serializers.CourseGroupUpstreamSerializer()
    statistics = ExamStatisticsSerializer()
    grades = ExamGradeRangeSerializer(many=True)

    class Meta:
        model = grades_models.Exam
        fields = (
            grades_models.Exam.exam_id.field.name,
            grades_models.Exam.course_group.field.name,
            grades_models.Exam.moed.field.name,
            grades_models.Exam.students_count.field.name,
            grades_models.Exam.failures_count.field.name,
            grades_models.Exam.EXAM_STATISTICS_RELATED_FIELD_NAME,
            grades_models.Exam.EXAM_GRADES_RELATED_FIELD_NAME,
        )
