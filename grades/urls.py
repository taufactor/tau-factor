from rest_framework import routers

from grades import views as grades_views


router = routers.DefaultRouter()
router.register("grades", grades_views.ExamView, basename="grades")
urlpatterns = router.urls
