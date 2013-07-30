from django.forms import ModelForm
from meet.models import Event, Message


class EventForm(ModelForm):
  class Meta:
    model = Event
    fields=['name', 'start_date', 'end_date', 'type_maj', 'type_min', 'description']
    localized_fields = ('start_date', 'end_date',)



class MessageForm(ModelForm):
  class Meta:
    model = Message
    localised_fields=('pub_date',)


