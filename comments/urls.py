from rest_framework import routers

from comments import views as comments_views


router = routers.DefaultRouter()
router.register("comments", comments_views.CourseCommentsView, basename="comments")
urlpatterns = router.urls
