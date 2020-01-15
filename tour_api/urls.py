from rest_framework import routers

from .views import PackageList

router = routers.SimpleRouter()
router.register(r'', PackageList, basename='package-tour')

urlpatterns = router.urls