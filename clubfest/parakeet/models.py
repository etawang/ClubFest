from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Club(models.Model):
    club_name = models.CharField(max_length=256, default='NoName')
    table_id = models.IntegerField()
    CATEGORY_CHOICES=(
        ('evnt', "Event Planning/Publications"),
        ('sprt', "Recreational Sports"),
        ('spcl', "Special Interest"),
        ('comm', "Community Service"),
        ('buzz', "Business/Career"),
        ('rlgn', "Religion"),
        ('cult', "Cultural"),
        ('arts',"Performing Arts"),
        ('chng', "Social Change"),
        ('sci', "Science/Technology"),
        ('othr', "Other")
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
    num_tables = models.IntegerField(default=0)

class Event(models.Model):
    emap = models.ForeignKey(Map)
