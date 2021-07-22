from rest_framework import routers

from ratings import views as ratings_views


public_router = routers.DefaultRouter()
public_router.register("ratings", ratings_views.CourseRatingsView, basename="ratings")
public_urlpatterns = public_router.urls

private_router = routers.DefaultRouter()
private_router.register("ratings", ratings_views.CourseRatingsPrivateView, basename="ratings-private")
private_urlpatterns = private_router.urls
