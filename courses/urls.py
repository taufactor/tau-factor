from rest_framework import routers

from courses import views as courses_views


router = routers.DefaultRouter()
router.register("courses", courses_views.CoursesGroupView, basename="course-groups")
router.register("courses", courses_views.CoursesInstanceView, basename="course-instances")
router.register("courses", courses_views.CoursesView, basename="courses")

urlpatterns = router.urls
