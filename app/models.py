from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from multiselectfield import MultiSelectField

# Create your models here.
class Worker(models.Model):

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )

    active = models.BooleanField(default=False)

    SOURCE_SITES = (
        ("http://www.avito.ru", "Avito"),
        ("http://www.move.ru", "Move"),
        ("http://www.arendator.ru", "Arendator"),
        ("http://www.mirkvartir.ru", "Mirkvartir"),
        ("http://www.sob.ru", "Sob"),
        ("http://www.zdanie.info","Zdanie"),
        ("http://www.moskva.gde.ru","MoskvaGde"),
        ("http://www.propokupki.ru", "Propokupki"),
        ("http://www.kvmeter.ru", "KvMeter"),
        ("http://www.comrent.ru", "Comrent")
    )
    source = MultiSelectField(choices = SOURCE_SITES)

    min_cost = models.FloatField(validators=[MinValueValidator(0.0)]) # little bit tricky
    max_cost = models.FloatField(validators=[MinValueValidator(0.0)])

    email = models.CharField(max_length=200)

    OBJECTS_AMOUNTS = (
        (10,10),
        (20,20),
        (30,30),
        (50,50),
        (100,100)
    )
    objects_amount = models.IntegerField(choices = OBJECTS_AMOUNTS)

    starting_time = models.TimeField()

    UPDATING_PERIODS = (
        (900,"15 min"),
        (3600,"1 hour"),
        (10800,"3 hours"),
        (86400,"1 day")
        )
    updating_period = models.IntegerField(choices=UPDATING_PERIODS)

    OBJECTS_TYPES = (
        (0,"Rent"),
        (1,"Sell")
    )
    objects_type = MultiSelectField(choices = OBJECTS_TYPES)

    name = models.CharField(max_length=200)

    def run(self):
        self.active = True
        self.save()

    def stop(self):
        self.active = False
        self.save()

    def __str__(self):
        return self.name
