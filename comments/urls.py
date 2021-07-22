from rest_framework import routers

from comments import views as comments_views

public_router = routers.DefaultRouter()
public_router.register("comments", comments_views.CourseCommentsView, basename="comments")
public_urlpatterns = public_router.urls

private_router = routers.DefaultRouter()
private_router.register("comments", comments_views.CourseCommentsPrivateView, basename="comments-private")
private_urlpatterns = private_router.urls
