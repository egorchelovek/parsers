from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone
from multiselectfield import MultiSelectField
from app.task import parse_and_report

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

    def activate(self):

        if self.state_active == True:
            return

        self.state_active = True
        self.save()

        parse_and_report(
        self.id,
        self.mailing_list,
        list(self.source_sites),
        list(self.objects_types),
        self.objects_amount,
        self.city,
        self.room_area_min,
        self.room_area_max,
        self.min_price_rent,
        self.max_price_rent,
        self.min_price_sell,
        self.max_price_sell,
        repeat = self.updating_period)

    def stop(self):

        if self.state_active == False:
            return

        self.state_active = False
        self.save()

        # TODO stop task feature

    def __str__(self):
        return self.name
