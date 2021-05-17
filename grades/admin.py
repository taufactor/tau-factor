from django.contrib import admin

from grades import models as grades_models


admin.site.register(grades_models.Exam)
admin.site.register(grades_models.ExamStatistics)
admin.site.register(grades_models.ExamGradeRange)
