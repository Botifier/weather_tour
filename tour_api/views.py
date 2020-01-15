from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Max

from .models import Package, Tour, Destination
from .serializers import TourSerializer


class PackageList(viewsets.ReadOnlyModelViewSet):

    ''' Fetch Packages between two given dates for a given danger score '''
    serializer_class = TourSerializer
    def get_queryset(self):
        start, end = self.request.query_params.get('start'), self.request.query_params.get('end')
        danger_score = self.request.query_params.get('danger_score')
        queryset = Tour.objects.select_related('package') \
        .filter(date__range=[start, end]) \
        .prefetch_related('package__destination') \
        .annotate(top_danger_score=Max('package__destination__danger_score')) \
        .filter(top_danger_score=danger_score)

        return queryset
 
