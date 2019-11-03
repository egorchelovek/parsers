from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone
from multiselectfield import MultiSelectField
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

class Worker(models.Model):

    name = models.CharField(max_length=200)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    created_date = models.DateTimeField(default=timezone.now)

    state_active = models.BooleanField(default=False)

    mailing_list = models.CharField(max_length=200)

    source_sites = MultiSelectField(choices = tuple(settings.SOURCE_SITES.items()))

    objects_amount = models.IntegerField(choices = tuple(settings.OBJECTS_AMOUNTS.items()))

    objects_types = MultiSelectField(choices = tuple(settings.OBJECTS_TYPES.items()))

    city = models.CharField(max_length=200, choices=tuple(settings.CITIES.items()))

    room_area_min = models.FloatField(validators=[MinValueValidator(0.0)])
    room_area_max = models.FloatField(validators=[MinValueValidator(0.0)])

    min_price_rent = models.FloatField(validators=[MinValueValidator(0.0)]) # little bit tricky
    max_price_rent = models.FloatField(validators=[MinValueValidator(0.0)])

    min_price_sell = models.FloatField(validators=[MinValueValidator(0.0)])
    max_price_sell = models.FloatField(validators=[MinValueValidator(0.0)])

    report_time = models.TimeField()

    updating_period = models.IntegerField(choices=tuple(settings.UPDATING_PERIODS.items()))

    task_id = models.IntegerField(default = 0)

        # TODO stop task feature

    def __str__(self):
        return self.name
