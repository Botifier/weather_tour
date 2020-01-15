from rest_framework import serializers
from .models import Range, Capital


class CapitalSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Capital
        fields = ('name', 'temperature', )


class RangeSerializer(serializers.ModelSerializer):
    capital_set = CapitalSerializer(many=True)
    
    class Meta:
        model = Range
        fields = ('capital_set', 'start', 'end',)
