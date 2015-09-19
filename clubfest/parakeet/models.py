from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Club(models.Model):
    table_id = models.IntegerField()
    category = models.CharField(max_length=256)

class Table(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    club = models.ForeignKey(Club)

class Map(models.Model):
    height = models.IntegerField()
    width = models.IntegerField()
    tables = ArrayField(
        ArrayField(
            models.IntegerField()
        ),
    )

class Event(models.Model):
    emap = models.ForeignKey(Map)
