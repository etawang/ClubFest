from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Club(models.Model):
    club_name = models.CharField(max_length=256)
    table_id = models.IntegerField()
    CATEGORY_CHOICES=(
        ('spts', "Sports"),
        ('buzz', "Business"),
        ('arts',"Performing Arts"),
        ('othr', "Other"),
    )
    category = models.CharField(max_length=4, choices=CATEGORY_CHOICES, default="othr")

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
