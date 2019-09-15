from django import forms
from .models import Worker

class WorkerForm(forms.ModelForm):

    class Meta:
        model = Worker
        fields = (
        'name',
        'state_active',
        'mailing_list',
        'source_sites',
        'objects_amount',
        'objects_types',
        'min_price_rent',
        'max_price_rent',
        'min_price_sell',
        'max_price_sell',
        'starting_time',
        'updating_period',
        )
