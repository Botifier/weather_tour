from config.celery import app
from celery.signals import worker_ready

from django.conf import settings

from .services import openweather
from .models import Range, Capital


@worker_ready.connect
@app.task(name="update_south_america_weather")
def update_south_america_weather(**kwargs):
    # See: http://bulk.openweathermap.org/sample/city.list.json.gz
    south_america_ids = getattr(settings, 'SOUTH_AMERICA_IDS', None)

    capitals = openweather.bulk_get_temperature_by_city_ids(south_america_ids)

    if capitals == []:
        return 'failed to update south american capitals'

    capitals.sort(key=lambda x: x['temperature'])

    for i, range_ in enumerate(Range.objects.all()):
        # step=3 and last element is first+step-1=first+2 
        start, end = i*3, i*3+2
        Range.objects.filter(pk=range_.pk).update(start=capitals[start]['temperature'], end=capitals[end]['temperature'])
        for capital in capitals[start:end+1]:
            capital['range'] = range_
            stored = Capital.objects.filter(openweather_id=capital['openweather_id']).update(**capital)
