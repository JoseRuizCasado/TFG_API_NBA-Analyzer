# Generated by Django 3.0.6 on 2020-06-10 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataBaseManager', '0006_auto_20200603_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='field_goals_miss',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='team',
            name='conceded_field_goals_miss',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='team',
            name='field_goals_miss',
            field=models.IntegerField(default=0),
        ),
    ]
