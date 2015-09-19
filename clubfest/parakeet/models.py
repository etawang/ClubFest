from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Club(models.Model):
    club_name = models.CharField(max_length=256)
    table_id = models.IntegerField()
    OTHER='othr'
    SPORTS="sprt"
    BUSINESS="buzz"
    ARTS="arts"
    CATEGORY_CHOICES=(
        (SPORTS, 'sprt'),
        (BUSINESS, 'buz'),
        (ARTS,'art'),
        (OTHER, 'othr'),
    )
    category = models.CharField(max_length=4, choices=CATEGORY_CHOICES, default=OTHER)

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
