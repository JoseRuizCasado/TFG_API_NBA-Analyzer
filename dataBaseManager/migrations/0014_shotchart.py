# Generated by Django 3.0.6 on 2020-08-11 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataBaseManager', '0013_player_cluster'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShotChart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chart', models.ImageField(upload_to='', verbose_name='Shot chart')),
            ],
        ),
    ]
