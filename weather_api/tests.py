import responses
import re

from django.urls import reverse
from django.test import override_settings

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Capital, Range


MOCK_WEATHER_API_RESPONSE = {
    'weather': [{
        'main': 'weather test condition'
    }],
    'main': {
        'temp': 60
    }
}

MOCK_FORECAST_API_RESPONSE = {
    'list': [
        {
            "main": {
                "temp": 70
            },
            "weather": [{
                "main": "forecast test condition"
            }],
            "dt_txt": "2020-01-1{} 21:00:00".format(i//5)
        } for i in range(31)
    ]
}

class TemperatureDetailTest(APITestCase):

    @responses.activate
    def test_get_temperature(self):
        responses.add(
            responses.GET, 
            re.compile('^http://api.openweathermap.org/data/2.5/weather'),
            json=MOCK_WEATHER_API_RESPONSE, 
            status=200
        )
        responses.add(
            responses.GET,
            re.compile('^http://api.openweathermap.org/data/2.5/forecast'),
            json=MOCK_FORECAST_API_RESPONSE, 
            status=200       
        )

        response = self.client.get(reverse('temperature-detail'), {
            'long': 0, 'lat': 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        # correct current weather       
        self.assertEqual(response.data['current']['temperature'], 60)
        self.assertEqual(response.data['current']['condition'], 'weather test condition')
        # 7 > 31/5 > 6
        self.assertEqual(len(response.data['forecast']), 6)
        # correct forecast
        self.assertEqual(response.data['forecast'][0]['temperature'], 70)
        self.assertEqual(response.data['forecast'][0]['condition'], 'forecast test condition')


class SouthAmericanWeatherList(APITestCase):
    
    def setUp(self):
        ranges = Range.objects.all()
        for i, capital in enumerate(Capital.objects.all()):
            capital.range = ranges[i//3]
            capital.save()

    def test_list_south_american_weather(self):
        response = self.client.get(reverse('southamerica-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # there are 4 ranges
        self.assertEqual(len(response.data), 4)
        # each range has 3 capitals
        for range_ in response.data:
            self.assertEqual(len(range_['capital_set']), 3)