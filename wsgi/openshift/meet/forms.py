from django.forms import ModelForm
from django import forms 
from meet.models import Event, Message
from django.contrib.auth.models import User
from gettext import gettext as _

from django.forms.util import ErrorList

class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return u''
        return u'<div class="errorlist">%s</div>' % ''.join([u'<div class="alert alert-error"><button type="button" class="close" data-dismiss="alert">&times;</button><strong>Error!</strong> %s</div>' % e for e in self])

class EventForm(ModelForm):
    class Meta:
        model = Event
    fields=['name', 'start_date', 'end_date', 'type_maj', 'type_min', 'description']
    localized_fields = ('start_date', 'end_date',)



class MessageForm(ModelForm):
    class Meta:
        model = Message
    localised_fields=('pub_date',)

# Copied from
# http://docs.nullpobug.com/django/trunk/django.contrib.auth.forms-pysrc.html
class UserRegistrationForm(ModelForm):
    #A form that creates a user, with no privileges, from the given username and password. 
    username = forms.RegexField(label=_("Username"), max_length=30,regex=r'^[\w.-]+$', 
            help_text = _("Required. 30 characters or fewer. Alphanumeric characters only (letters, digits and underscores)."), 
            error_message = _("This value must contain only letters, numbers and underscores.")) 
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput) 
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput) 
    class Meta: 
        model = User 
        fields = ("username","first_name", "last_name", "email", "password1", "password2") 


def clean_username(self): 
    username = self.cleaned_data["username"] 
    try: 
        User.objects.get(username=username) 
    except User.DoesNotExist: 
        return username 
    raise forms.ValidationError(_("A user with that username already exists.")) 

def clean_password2(self): 
    password1 = self.cleaned_data.get("password1", "") 
    password2 = self.cleaned_data["password2"] 
    if password1 != password2: 
        raise forms.ValidationError(_("The two password fields didn't match.")) 
    return password2 

def save(self, commit=True): 
    user = super(UserRegistrationForm, self).save(commit=False) 
    user.set_password(self.cleaned_data["password1"]) 
    if commit: 
        user.save() 
    return user 



