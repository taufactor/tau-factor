from rest_framework import routers

from grades import views as grades_views


public_router = routers.DefaultRouter()
public_router.register("grades", grades_views.ExamView, basename="grades")
public_urlpatterns = public_router.urls

private_router = routers.DefaultRouter()
private_router.register("grades", grades_views.ExamPrivateView, basename="grades-private")
private_urlpatterns = private_router.urls
