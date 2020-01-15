from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from .services import openweather
from .models import Capital, Range
from .serializers import RangeSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class TemperatureDetail(APIView):
    
    ''' get current weather from lat and longitude '''
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        latitude = self.request.query_params.get('lat')
        longitude = self.request.query_params.get('long')
        return Response(openweather.get_current_and_forecast(lat=latitude, long=longitude))


class SouthAmericanWeatherList(viewsets.ReadOnlyModelViewSet):

    ''' get the temperatures of south american capitals and group them '''
    queryset = Range.objects.prefetch_related('capital_set').all()
    serializer_class = RangeSerializer
