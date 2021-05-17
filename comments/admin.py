from django.contrib import admin

from comments import models as comments_models


admin.site.register(comments_models.CourseComment)
