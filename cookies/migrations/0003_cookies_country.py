# Generated by Django 3.0.7 on 2020-06-19 09:57

from django.db import migrations, models

from cookies.models import Cookies
from django.contrib.gis.geoip2 import GeoIP2

def set_my_defaults(apps, schema_editor):
    Cookies = apps.get_model('cookies', 'Cookies')
    for cookie in Cookies.objects.all().iterator():
        g = GeoIP2()
        cookie.country = g.country_name(cookie.ip)
        cookie.save()

def reverse_func(apps, schema_editor):
    pass  # code for reverting migration, if any

class Migration(migrations.Migration):

    dependencies = [
        ('cookies', '0002_auto_20200612_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='cookies',
            name='country',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.RunPython(set_my_defaults, reverse_func),
    ]
