from django.db import models

# Create your models here.
class Club(models.Model):
    table = models.ForeignKey(Table)
    category = models.CharField(max_length=256)

class Table(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    club = models.ForeginKey(Club)

class Map(models.Model):
    height = models.IntegerField()
    width = models.IntegerField()
    tables = ArrayField(
        ArrayField(
            models.IntegerField()
        ),
    )
