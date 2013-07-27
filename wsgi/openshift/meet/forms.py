from django.forms import ModelForm
from meet.models import Event


class EventForm(ModelForm):
  class Meta:
    model = Event
    fields=['name', 'start_date', 'end_date', 'type_maj', 'type_min', 'description']
    localized_fields = ('start_date', 'end_date',)
