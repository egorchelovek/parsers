from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone
from multiselectfield import MultiSelectField

# Create your models here.
class Worker(models.Model):

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    created_date = models.DateTimeField(default=timezone.now)

    active = models.BooleanField(default=False)

    source = MultiSelectField(choices = settings.SOURCE_SITES)

    min_cost = models.FloatField(validators=[MinValueValidator(0.0)]) # little bit tricky
    max_cost = models.FloatField(validators=[MinValueValidator(0.0)])

    email = models.CharField(max_length=200)

    objects_amount = models.IntegerField(choices = settings.OBJECTS_AMOUNTS)

    starting_time = models.TimeField()

    updating_period = models.IntegerField(choices=settings.UPDATING_PERIODS)

    objects_type = MultiSelectField(choices = settings.OBJECTS_TYPES)

    name = models.CharField(max_length=200)

    def run(self):
        self.active = True
        self.save()

    def stop(self):
        self.active = False
        self.save()

    def __str__(self):
        return self.name
