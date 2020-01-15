from rest_framework import serializers

from .models import Package, Tour, Destination


class DestinationSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city')
    
    class Meta:
        model = Destination
        fields = ('city_name', 'destination_type',)


class TourSerializer(serializers.ModelSerializer):
    package_name = serializers.CharField(source='package.name')
    price = serializers.FloatField(source='package.price')
    package_description = serializers.CharField(source='package.description')
    destinations = DestinationSerializer(source='package.destination', many=True)
    
    class Meta:
        model = Tour
        fields = ('package_name', 'price', 'package_description', 'date', 'capacity', 'destinations')


