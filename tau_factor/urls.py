from django.contrib import admin
from django import urls
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from tau_factor import settings

schema_view = get_schema_view(
   openapi.Info(
       url=f"https://{settings.SITE_URL}/api/{settings.API_VERSION}/",
       title=f"{settings.SITE_NAME_EN} API",
       default_version='v1',
       description=f"""This documentation describes the backend API for {settings.SITE_NAME_EN}.
                       Using this API, you can retrieve course information, as well as past exam grades,
                       and user comments and ratings for the different courses.""",
       terms_of_service="https://www.google.com/policies/terms/",
       contact=openapi.Contact(email="contact@snippets.local"),
       license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    urls.path("admin/", admin.site.urls),
    urls.re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name='schema-json'),
    urls.re_path(r"^swagger/$", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    urls.re_path(r"^redoc/$", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    urls.path("", urls.include("fe.urls")),
    urls.path(f"api/{settings.API_VERSION}/", urls.include("comments.urls")),
    urls.path(f"api/{settings.API_VERSION}/", urls.include("courses.urls")),
    urls.path(f"api/{settings.API_VERSION}/", urls.include("extension.urls")),
    urls.path(f"api/{settings.API_VERSION}/", urls.include("grades.urls")),
    urls.path(f"api/{settings.API_VERSION}/", urls.include("ratings.urls")),
]

