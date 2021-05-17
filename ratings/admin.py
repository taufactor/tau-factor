from django.contrib import admin

from ratings import models as ratings_models


admin.site.register(ratings_models.CourseRating)
