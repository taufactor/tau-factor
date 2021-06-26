from rest_framework import routers

from extension import views as extension_views


router = routers.DefaultRouter()
router.register("extension", extension_views.ExtensionView, basename="extension")

urlpatterns = router.urls
