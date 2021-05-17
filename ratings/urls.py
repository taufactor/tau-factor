from rest_framework import routers

from ratings import views as ratings_views


router = routers.DefaultRouter()
router.register("ratings", ratings_views.CourseRatingsView, basename="ratings")
urlpatterns = router.urls
