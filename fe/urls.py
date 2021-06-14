from django import urls

from fe import views as frontend_views

urlpatterns = urls.path('', frontend_views.index, name='index'),
