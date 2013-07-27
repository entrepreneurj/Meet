# widgets.py
from django import forms
from django.db import models
from django.template.loader import render_to_string
from django.forms.widgets import Select, MultiWidget, DateInput, TextInput, TimeInput
from time import strftime


class HTML5TimeInput(TimeInput):
    def __init__(self, itype, attrs):
        self.input_type = itype
        super(HTML5TimeInput, self).__init__(attrs)

class HTML5DateInput(DateInput):
    def __init__(self, itype, attrs, format):
        self.input_type = itype
        super(HTML5DateInput, self).__init__(attrs)


class JqSplitDateTimeWidget(MultiWidget):

    def __init__(self, attrs=None, date_format=None, time_format=None):
        date_class = attrs['date_class']
        time_class = attrs['time_class']
        del attrs['date_class']
        del attrs['time_class']

        time_attrs = attrs.copy()
        time_attrs['class'] = time_class
    
        date_attrs = attrs.copy()
        date_attrs['class'] = date_class

        widgets = (HTML5DateInput(itype="date", attrs=date_attrs, format=date_format), HTML5TimeInput(itype="time", attrs=time_attrs))

        super(JqSplitDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            d = strftime("%Y-%m-%d", value.timetuple())
            hour = strftime("%H", value.timetuple())
            minute = strftime("%M", value.timetuple())
            meridian = strftime("%p", value.timetuple())
            return (d, hour+":"+minute, meridian)
        else:
            return (None, None, None)

    def format_output(self, rendered_widgets):
        """
        Given a list of rendered widgets (as strings), it inserts an HTML
        linebreak between them.

        Returns a Unicode string representing the HTML for the whole lot.
        """
        return "Date: %s<br/>Time: %s" % (rendered_widgets[0], rendered_widgets[1])


    class Media:
        css = {
            }
        js = (
            "js/jqsplitdatetime.js",
            )
