# Generated by Django 3.0.6 on 2020-08-11 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataBaseManager', '0014_shotchart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shotchart',
            name='id',
        ),
        migrations.AddField(
            model_name='shotchart',
            name='pf',
            field=models.IntegerField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
