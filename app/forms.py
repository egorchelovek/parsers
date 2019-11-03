from django import forms
from .models import Worker

class WorkerForm(forms.ModelForm):

    class Meta:
        model = Worker
        fields = (
        'name',
        'mailing_list',
        'source_sites',
        'objects_amount',
        'objects_types',
        'city',
        'room_area_min',
        'room_area_max',
        'min_price_rent',
        'max_price_rent',
        'min_price_sell',
        'max_price_sell',
        'report_time',
        'updating_period',
        )
