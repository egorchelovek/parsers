from django import forms
from .models import Worker

class WorkerForm(forms.ModelForm):

    class Meta:
        model = Worker
        fields = ('source', 'min_cost', 'max_cost', 'email', 'objects_amount', 'starting_time', 'updating_period', 'name')
