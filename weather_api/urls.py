from django.conf.urls import url
from rest_framework import routers

from .views import TemperatureDetail, SouthAmericanWeatherList

router = routers.SimpleRouter()
router.register(r'south-america', SouthAmericanWeatherList, basename='southamerica')

urlpatterns = router.urls + [
    url('temperature/', TemperatureDetail.as_view(), name="temperature-detail"),
]