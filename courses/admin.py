from django.contrib import admin

from courses import models as courses_models


admin.site.register(courses_models.Course)
admin.site.register(courses_models.CourseCommonName)

admin.site.register(courses_models.CourseInstance)
admin.site.register(courses_models.CourseInstanceName)

admin.site.register(courses_models.CourseGroup)
admin.site.register(courses_models.CourseGroupTeacher)
