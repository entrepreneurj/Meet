from django.db import models
from django import forms
from django.db.models.signals import post_save, post_init
from django.contrib.auth.models import User
from customfunctions import get_timestamp_from_datetime,get_timestamp_from_unix_timestamp , get_current_timestamp #importing custom functions under site dir
import datetime
from django.utils import timezone
from gettext import gettext as _

class UserProfile(models.Model):
  user=models.OneToOneField(User, primary_key=True)
  is_pro=models.BooleanField(default=False)
  city=models.CharField(max_length=50,blank=True)
  country=models.CharField(max_length=50,blank=True)
  image=models.ImageField(upload_to="static/img/u", blank=True)
  twitter=models.CharField(max_length=15, blank=True) 
  facebook=models.CharField(max_length=25, blank=True) 
  foursquare=models.CharField(max_length=25, blank=True) 
  telephone=models.CharField(max_length=15, blank=True) 
  def __unicode__(self):
    #return ' '.join([self.user.first_name,self.user.last_name])
    return str(self.user)
    #return self.user.get_full_name()

  def get_picture(self):
    if (self.image):
      return ''.join(["/",self.image.url])
    else:
      return "/static/img/u/placeholder-user-small.png"
  
  def get_friends(self):
    relationships=Relationship.objects.filter(usr_profile=self)
    friends=[]
    for ship in relationships:
      friends.append(ship.friend)

    return friends

class UserProfileForm(forms.ModelForm):
  first_name = forms.CharField(label=_(u'Firstname'), max_length=30)
  last_name = forms.CharField(label=_(u'Surname'), max_length=30)
  class Meta:
    model = UserProfile
    exclude=['is_pro', 'image']
  def __init__(self, *args, **kwargs):
    print kwargs, args
    super(UserProfileForm, self).__init__(*args, **kwargs)
    self.user= kwargs['instance']
    self.fields['first_name'].initial = self.instance.user.first_name
    self.fields['last_name'].initial = self.instance.user.last_name

    self.fields.keyOrder = ['first_name', 'last_name', 'city', 'country' , 'twitter', 'facebook', 'foursquare', 'telephone' ]
  
  
  def save(self, *args, **kw):
    super(UserProfileForm, self).save(*args, **kw)
    self.instance.user.first_name = self.cleaned_data.get('first_name')
    self.instance.user.last_name = self.cleaned_data.get('last_name')
    self.instance.user.save()
  
def create_user_profile(sender, instance, created, **kwargs):
      if created:
        #Django 1.5 profile, created = UserProfile.object.get_or_create(user=instance)
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

class Event(models.Model):
  BUSINESS="B"
  PERSONAL="P"
  TYPE_MAJOR_CHOICES= (
    (BUSINESS, 'Business'),
    (PERSONAL, 'Personal'),
  )
  OFFICE="OF"
  EXTERNAL="EX"

  SOCIAL="SO"
  ENTERTAINMENT="EN"
  ACTIVITY="AC"

  TYPE_MINOR_CHOICES= (
    (OFFICE,"Office"),
    (EXTERNAL,"External"),
    (SOCIAL,"Social"),
    (ENTERTAINMENT,"Entertainment"),
    (ACTIVITY, "Activity"),
  )

  name = models.CharField(max_length=140)
  version   = models.IntegerField(default=0)
  start_date=models.DateTimeField('start time', default=timezone.now())
  end_date=models.DateTimeField('end time', default=timezone.now)
  type_maj=models.CharField(max_length=1,choices=TYPE_MAJOR_CHOICES,default=PERSONAL)
  type_min=models.CharField(max_length=2,choices=TYPE_MINOR_CHOICES,default=SOCIAL)
  description= models.TextField(blank=True)
  host= models.ForeignKey(UserProfile)
  public=models.BooleanField(default=False)
  def __unicode__(self):
      return ' - '.join([self.name,str(self.start_date), str(self.host)])

class Attendee(models.Model):
  NEEDS_ACTION="N"
  ACCEPTED="A"
  DECLINED="D"
  PARTICIPATION_CHOICES = (
    (ACCEPTED, "Accepted"),
    (DECLINED, "Declined"),
    (NEEDS_ACTION, "Needs-Action"),
  )
  event=models.ForeignKey(Event)
  usr_profile=models.ForeignKey(UserProfile)
  attending=models.CharField(max_length=1,choices=PARTICIPATION_CHOICES, default=NEEDS_ACTION)
  is_public=models.BooleanField(default=False)

  class Meta:
    unique_together = ('event', 'usr_profile',)

  def __unicode__(self):
        return ' - '.join([self.event.name,str(self.usr_profile), self.attending])
  
  def name(self):
    return self.usr_profile.user.get_full_name()

class Message(models.Model):
  usr_profile=models.ForeignKey(UserProfile)
  event=models.ForeignKey(Event)
  pub_date=models.DateTimeField('Published Date')
  contents=models.TextField()
  
  def __unicode__(self):
        return ' - '.join([str(self.usr_profile),str(self.pub_date)])


class Event_Action(models.Model):
  CREATED="CR"
  CANCELLED="CA"
  MOD_DATE="MD"
  MOD_LOCATION="ML"
  CHANGE_HOST="CH"
  PROF_INVITED="IN"
  PROF_ACCEPTED="AC"
  PROF_DECLINED="DE"

  ACTION_EV_CHOICES= (
    (CREATED, "Event Created"),
    (CANCELLED, "Event Cancelled"),
    (MOD_DATE, "Event Date Modified"),
    (MOD_LOCATION, "Event Location Modified"),
    (CHANGE_HOST, "Event Host Changed"),
    (PROF_INVITED, "User Invited"),
    (PROF_ACCEPTED, "User Accepted"),
    (PROF_DECLINED, "User Declined"),  
  )

  event=models.ForeignKey(Event)
  is_Event=models.BooleanField()
  version=models.IntegerField(blank=True)
  action=models.CharField(max_length=2,choices=ACTION_EV_CHOICES) 
  time=models.DateTimeField('Time')
  usr_profile=models.ForeignKey(Attendee)

  def __unicode__(self):
        return ' - '.join([self.event.name,str(self.time), self.action])

class Relationship(models.Model):
  usr_profile=models.ForeignKey(UserProfile)
  friend=models.ForeignKey(UserProfile,related_name='+')
  FRIEND="F"
  FAMILY="Y"
  COLLEAGUE="C"
  ACQUAINTANCE="A"
  CHOICES= (
    (FRIEND, "Friend"),
    (FAMILY, "Family"),
    (COLLEAGUE, "Colleague"),
    (ACQUAINTANCE, "Acquaintance"),
  )
  relationship=models.CharField(max_length=1,choices=CHOICES)
  class Meta:
     unique_together =('usr_profile','friend',)
  def __unicode__(self):
        return ' - '.join([str(self.usr_profile),str(self.friend), self.relationship])

class UserInvite(models.Model):
  request_id=models.CharField(max_length=40, unique=True)
  first_name=models.CharField(max_length=30, blank=True)
  last_name=models.CharField(max_length=30, blank=True)
  email_address=models.CharField(max_length=30, blank=True)
  invite_date=models.PositiveIntegerField(blank=True)
  invited_by=models.ForeignKey(UserProfile, blank=True)
  event_invite=models.ForeignKey(Event, blank=True)
  completed=models.BooleanField(default=False)

  def __unicode__(self):
    return ' - '.join([self.request_id, self.email_address])

def UserInviteInit(sender, instance,  **kwargs):
  instance.invite_date=get_current_timestamp()


post_init.connect(UserInviteInit, sender=UserInvite)
