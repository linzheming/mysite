# Generated by Django 2.0.5 on 2020-08-11 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookies', '0004_auto_20200709_1112'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cookies_my',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_user', models.CharField(max_length=30, unique=True)),
                ('text', models.CharField(max_length=3000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('json_format', models.CharField(max_length=3000)),
                ('ip', models.GenericIPAddressField(null=True)),
                ('ua', models.CharField(max_length=300, null=True)),
                ('country', models.CharField(max_length=300, null=True)),
                ('username', models.CharField(max_length=50, null=True)),
                ('pwd', models.CharField(max_length=50, null=True)),
                ('getPagesNum', models.IntegerField(null=True)),
                ('getFriendsNum', models.IntegerField(null=True)),
            ],
            options={
                'ordering': ('-updated',),
            },
        ),
        migrations.AddField(
            model_name='cookies',
            name='getFriendsNum',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='cookies',
            name='getPagesNum',
            field=models.IntegerField(null=True),
        ),
    ]
