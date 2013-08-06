# Create your views here.
from django.core.context_processors import csrf
from meet.models import *
from django.shortcuts import render, render_to_response, redirect
from django.views.generic import DetailView
#Django 1.5 from django.contrib.auth import get_user_model
from django.contrib.auth.models import User #Django < 1.5
from django.template import RequestContext
from meet.forms import *
from meet.admin import UserProfileAdmin
from pprint import pprint
from django.utils import timezone
from django.contrib import messages
from datetime import datetime
from django.contrib.auth import authenticate, login
from api.views import event_invite

def home(request):
    #return render_to_response('home/home.html')
        return render_to_response('splash.html',  context_instance=RequestContext(request))
### Login Views

#@login_required
def accountform(request):
    data = {}
    data.update(csrf(request))
    user_profile = request.user.get_profile()
    data['form'] = UserProfileForm(instance=user_profile)
    return render(request, 'accountform.html', data)


class UserProfileDetailView(DetailView):
  model = User # UserProfile
  slug_field = "username"
  template_name= "user_detail.html"


  def get_object(self, queryset=None):
  #Always creates the profile before retreiving the object
    user = super(UserProfileDetailView, self).get_object(queryset)
    UserProfile.objects.get_or_create(user=user)
   # Django >=1.5 UserProfile.objects.get_or_create(user=get_user_model())
    return user


def profile(request, slug):
  user=User.objects.filter(username=slug)[0]
  user_profile, created=UserProfile.objects.get_or_create(user=user)
  if (request.POST.get('fname',"") ):
    user_profile.user.first_name=request.POST.get('fname',"")   
    user_profile.user.last_name=request.POST.get('lname',"")
    user_profile.user.save()
 # if (request.POST.get('city',"") or request.POST.get('country',"") ):
 #   user_profile.city=request.POST.get('city',"")
 #   user_profile.country=request.POST.get('country',"")
 #   user_profile.save()
  if (request.user == user):
    is_me=True
  else:
    is_me=False

  return render_to_response('user_detail.html', { 'object':user_profile.user, 'is_me':is_me}, context_instance=RequestContext(request) )

def profile_edit(request, slug):
  user=User.objects.filter(username=slug)[0]
  user_profile, created=UserProfile.objects.get_or_create(user=user)
  if (request.user == user):
    is_me=True
    if (request.POST ):
      #f=UserProfileAdmin(request.POST, user_profile)
      f=UserProfileForm(request.POST,instance=user_profile)
      f.save()
      #user_profile.save()
      return redirect("profile", slug=user.username)
    else:
      UsrProfileFrm=UserProfileForm(instance=user_profile)
      return render_to_response('user_edit.html', { 'object':user_profile.user, 'form':UsrProfileFrm}, context_instance=RequestContext(request) )
  else:
    is_me=False
    return redirect("profile_edit", slug=request.user.username)

def profile_events(request, slug):
  user=User.objects.filter(username=slug)[0]
  usr_profile, created=UserProfile.objects.get_or_create(user=user)
  events=Event.objects.filter(public=True, attendee__is_public=True, attendee__usr_profile=usr_profile)
  if (events):
    return render_to_response('user_events.html', {'events':events, 'user':user }, context_instance=RequestContext(request) )
  else:
    return render_to_response('user_events.html', { 'user':user }, context_instance=RequestContext(request) )

### Main views

def dashboard(request):

  user_profile, created =UserProfile.objects.get_or_create(user=request.user)
  events=Event.objects.filter(attendee__usr_profile=user_profile)
  if (events):
    return render_to_response('dashboard.html', {'events':events, }, context_instance=RequestContext(request) )
  else:

    return render_to_response('dashboard.html', context_instance=RequestContext(request) )


def friends(request, slug):
  user=User.objects.filter(username=slug)[0]
  usr_profile=user.get_profile()
  friends=usr_profile.get_friends()

  return render_to_response('friends.html', {'friends':friends, 'user':user }, context_instance=RequestContext(request) )
### User ###


def user_invite(request,timestamp,request_id):
    if (request.POST):
        uf = UserRegistrationForm(request.POST, error_class=DivErrorList)
        if uf.is_valid():
            user = uf.save(commit=False)
            user.set_password(request.POST.get('password1',''))
            user.save()
            user=authenticate(username=uf.data['username'],password=request.POST.get('password1',''))
            invites=UserInvite.objects.filter(email_address=request.POST.get('email',''))
            for inv in invites:
                if inv.event_invite:
                    event_invite(user.username, inv.event_invite)
                if inv.invited_by:
                    pass
                    #insert friend request from user        
            login(request, user)
            return redirect('dashboard')
        else:
            print "error", uf.errors, uf;
            return render_to_response('user_signup_invite.html',{
                'form':uf}, context_instance=RequestContext(request) )
    invite_date=datetime.fromtimestamp(float(timestamp))
    invite=UserInvite.objects.filter(request_id=request_id, invite_date=timestamp)
    print invite;
    if (invite):
        u=UserRegistrationForm(initial={'email':invite[0].email_address,
            'first_name': invite[0].first_name, 'last_name':invite[0].last_name})
        return render_to_response('user_signup_invite.html',{'invite':invite, 'form':u}, context_instance=RequestContext(request) )
    else:
        return redirect("home")

### Events ###
def create_event(request):
  if (request.POST):
    f=EventForm(request.POST)
    new_Event=f.save(commit=False)
    host, created = UserProfile.objects.get_or_create(user=request.user)
    new_Event.host=host
    new_Event.save()
    host_attendee=Attendee();
    host_attendee.usr_profile=new_Event.host;
    host_attendee.event=new_Event;
    host_attendee.attending="A";
    host_attendee.save()
    messages.add_message(request, messages.INFO,"Your meet was created successfully. Invite a friend", extra_tags='alert-success')
    return redirect('event_detail', slug=new_Event.id )
  
  else:  
    return render_to_response('create_event.html', {'form':EventForm()},context_instance=RequestContext(request) )

def event_detail(request, slug):
  user=request.user.get_profile()
  event = Event.objects.get(id=slug)
  my_att=list(Attendee.objects.filter(usr_profile=user, event=event))
  if (request.POST.get('contents',"")  ):
    #f=MessageForm(request.POST)
    #new_msg=f.save(commit=False);
    new_msg=Message();
    new_msg.contents=request.POST.get('contents',"") 
    new_msg.event=event;
    new_msg.usr_profile=user;
    new_msg.pub_date=timezone.now()
    new_msg.save()

  if (my_att):
    return render_to_response('event_detail.html', {'event':event, 'personal_att':my_att[0]},context_instance=RequestContext(request) )
  else:
    return render_to_response('event_detail.html', {'event':event},context_instance=RequestContext(request) )

def event_edit(request, slug):
  user=request.user.get_profile()
  event = Event.objects.get(id=slug)
  if (event.host==user):
    #from django.core.mail import send_mail

    #send_mail('Subject here', 'Here is the message.', 'technical@icradio.com',
    #        ['technical@icradio.com'], fail_silently=False)
    return render_to_response('event_edit.html', {'event':event},context_instance=RequestContext(request) )
  else:
    redirect('event_detail', slug=slug)
