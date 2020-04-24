from django.db import models

# Create your models here.
class Song (models.Model):
    id = models.BigIntegerField(primary_key=True, null=False)
    artist = models.CharField(max_length=255, null=False)
    title = models.CharField(max_length=255, null=False)

    def __str__(self):
        return  f'(id: {self.id}, artist: {self.artist}, title:{self.title})'
