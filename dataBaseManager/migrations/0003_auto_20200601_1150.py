# Generated by Django 3.0.6 on 2020-06-01 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataBaseManager', '0002_auto_20200601_1134'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ['team_id'], 'verbose_name': 'Player', 'verbose_name_plural': 'Players'},
        ),
        migrations.RenameField(
            model_name='player',
            old_name='name',
            new_name='first_name',
        ),
    ]
