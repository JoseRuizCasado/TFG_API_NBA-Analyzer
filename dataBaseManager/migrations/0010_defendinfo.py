# Generated by Django 3.0.6 on 2020-08-03 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataBaseManager', '0009_game_information_loaded'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefendInfo',
            fields=[
                ('auto_increment_id', models.AutoField(primary_key=True, serialize=False)),
                ('shooter_id', models.IntegerField()),
                ('shooter_position', models.CharField(choices=[('PG', 'Pointguard'), ('SG', 'Shootingguard'), ('SF', 'Smallforward'), ('PF', 'Powerforward'), ('C', 'Center')], max_length=255)),
                ('defender_id', models.IntegerField()),
                ('defend_success', models.BooleanField()),
                ('shooter_cluster', models.IntegerField()),
            ],
        ),
    ]
