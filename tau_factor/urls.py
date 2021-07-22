from django.contrib import admin
from django import urls
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from comments import urls as comments_urls
from courses import urls as courses_urls
from grades import urls as grades_urls
from ratings import urls as ratings_urls
from tau_factor import settings

public_app_urlpatterns = [
    urls.path(f"api/{settings.API_VERSION}/", urls.include(comments_urls.public_urlpatterns)),
    urls.path(f"api/{settings.API_VERSION}/", urls.include(courses_urls.public_urlpatterns)),
    urls.path(f"api/{settings.API_VERSION}/", urls.include(grades_urls.public_urlpatterns)),
    urls.path(f"api/{settings.API_VERSION}/", urls.include(ratings_urls.public_urlpatterns)),
]

public_schema_view = get_schema_view(
    openapi.Info(
        url=f"https://{settings.SITE_URL}/api/{settings.API_VERSION}/",
        title=f"{settings.SITE_NAME_EN} API",
        default_version='v1',
        description=f"""This documentation describes the backend API for {settings.SITE_NAME_EN}.
                        Using this API, you can retrieve course information, as well as past exam grades,
                        and user comments and ratings for the different courses.""",
        contact=openapi.Contact(email="factor.tau@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=public_app_urlpatterns,
)

public_swagger_urlpatterns = [
    urls.re_path(r"^swagger(?P<format>\.json|\.yaml)$", public_schema_view.without_ui(cache_timeout=0), name='schema-json'),
    urls.re_path(r"^swagger/$", public_schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    urls.re_path(r"^redoc/$", public_schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

private_app_urlpatterns = [
    urls.path(f"api/{settings.API_VERSION}/", urls.include(comments_urls.private_urlpatterns)),
    urls.path(f"api/{settings.API_VERSION}/", urls.include(courses_urls.private_urlpatterns)),
    urls.path(f"api/{settings.API_VERSION}/", urls.include("extension.urls")),
    urls.path(f"api/{settings.API_VERSION}/", urls.include(grades_urls.private_urlpatterns)),
    urls.path(f"api/{settings.API_VERSION}/", urls.include(ratings_urls.private_urlpatterns)),
]


private_schema_view = get_schema_view(
    openapi.Info(
        url=f"https://{settings.SITE_URL}/api/{settings.API_VERSION}/",
        title=f"{settings.SITE_NAME_EN} API",
        default_version='v1',
        description=f"""This documentation describes the backend API for {settings.SITE_NAME_EN}.
                        Using this API, you can retrieve course information, as well as past exam grades,
                        and user comments and ratings for the different courses.""",
        contact=openapi.Contact(email="factor.tau@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=public_app_urlpatterns + private_app_urlpatterns,
)

private_swagger_urlpatterns = [
    urls.re_path(r"^full_swagger(?P<format>\.json|\.yaml)$", private_schema_view.without_ui(cache_timeout=0), name='schema-json'),
    urls.re_path(r"^full_swagger/$", private_schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    urls.re_path(r"^full_redoc/$", private_schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns = [
    urls.path("admin/", admin.site.urls),
    urls.path("", urls.include("fe.urls")),
] + private_app_urlpatterns + private_swagger_urlpatterns + public_app_urlpatterns + public_swagger_urlpatterns
