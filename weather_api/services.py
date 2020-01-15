import requests

from statistics import mean
from collections import Counter
from django.conf import settings


class OpenWeather:
    BASE_URL = 'http://api.openweathermap.org/data/2.5'
    CURRENT_WEATHER_URL = BASE_URL + '/weather?units=metric&lat={}&lon={}'
    WEATHER_FORECAST_URL = BASE_URL + '/forecast?units=metric&lat={}&lon={}'
    WEATHER_BY_ID_URL = BASE_URL + '/weather?units=metric&id={}'

    def __init__(self, app_id=None):        
        self.app_id = app_id
    
    def _query(self, url):
        response = requests.get(url, params={'APPID': self.app_id})
        if response.ok:
            return response.json()
        else:
            return None

    def get_current_and_forecast(self, lat, long):
        return {
            'current': self._get_current_weather(lat, long),
            'forecast': self._average_daily(self._get_weather_forecast(lat,long)),
        }

    def _get_current_weather(self, lat, long):
        data = self._query(self.CURRENT_WEATHER_URL.format(lat, long))
        return {
            'temperature': data['main']['temp'],
            'condition': data['weather'][0]['main'],
        }
    
    def _get_weather_forecast(self, lat, long):
        data = self._query(self.WEATHER_FORECAST_URL.format(lat, long))['list']
        return self._group_data_by_day(data)
    
    def _group_data_by_day(self, data):
        result = {}
        last_date = data[0]['dt_txt'][:10]
        current_date_data = [
            {
                'temperature': data[0]['main']['temp'],
                'condition': data[0]['weather'][0]['main'],
            }
        ]
        for forecast in data[1:]:
            current_date = forecast['dt_txt'][:10]
            if current_date != last_date:
                result[current_date] = current_date_data
                current_date_data = []

            current_date_data.append(
                {
                    'temperature': forecast['main']['temp'],
                    'condition': forecast['weather'][0]['main'],
                }
            )
            last_date = current_date

        return result
    
    def _average_daily(self, data):
        result = []
        
        for day in data:
            result.append(
                {
                    'temperature': mean([x['temperature'] for x in data[day]]),
                    'condition': Counter([x['condition'] for x in data[day]]).most_common()[0][0],
                }
            )
         
        return result   
    
    def bulk_get_temperature_by_city_ids(self, ids):
        urls  = [self.WEATHER_BY_ID_URL.format(city_id) for city_id in ids]
        responses = [self._query(url) for url in urls]
        if all([res is not None for res in responses]):
            return [
                {
                    'temperature': res['main']['temp'],
                    'name': res['name'],
                    'openweather_id': res['id'],
                }
                for res in responses
            ]
        else:
            return []


openweather = OpenWeather(getattr(settings, 'OPEN_WEATHER_APP_ID', None))
