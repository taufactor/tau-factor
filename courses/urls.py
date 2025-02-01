from rest_framework import routers

from courses import views as courses_views


public_router = routers.DefaultRouter()
public_router.register("courses", courses_views.CoursesView, basename="courses")
public_router.register("courses_instances", courses_views.CoursesInstanceView, basename="course-instances")
public_urlpatterns = public_router.urls

private_router = routers.DefaultRouter()
private_router.register("courses", courses_views.CoursesGroupView, basename="course-groups")
private_router.register("courses", courses_views.CoursesInstancePrivateView, basename="course-instances")
private_urlpatterns = private_router.urls
