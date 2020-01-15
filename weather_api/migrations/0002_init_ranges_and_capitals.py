from django.db import migrations
from django.conf import settings


def init_db(apps, schema_editor):
    Range = apps.get_model('weather_api', 'Range')
    Capital = apps.get_model('weather_api', 'Capital')

    # init empty ranges:
    Range.objects.bulk_create([Range(start=0, end=0)] * 4)

    # init capital ids
    south_america_ids = getattr(settings, 'SOUTH_AMERICA_IDS', None)

    Capital.objects.bulk_create(
        [
            Capital(
                name='name', 
                temperature=0, 
                range=Range.objects.first(),
                openweather_id=id
            )
            for id in south_america_ids    
        ]
    )


class Migration(migrations.Migration):

    dependencies = [
        ('weather_api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(init_db, migrations.RunPython.noop),
    ]

