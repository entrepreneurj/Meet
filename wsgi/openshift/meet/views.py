# Create your views here.
from django.core.context_processors import csrf
from meet.models import *
from django.shortcuts import render, render_to_response, redirect
from django.views.generic import DetailView
#Django 1.5 from django.contrib.auth import get_user_model
from django.contrib.auth.models import User #Django < 1.5
from django.template import RequestContext
from meet.forms import *
from pprint import pprint


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
    print user_profile
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

### Main views

def dashboard(request):

  user_profile = request.user.get_profile()
  events=Event.objects.filter(attendee__usr_profile=user_profile)

  return render_to_response('dashboard.html', {'events':events, }, context_instance=RequestContext(request) )



def friends(request, slug):
  user=User.objects.filter(username=slug)[0]
  usr_profile=user.get_profile()
  friends=usr_profile.get_friends()

  print friends
  return render_to_response('friends.html', {'friends':friends, 'user':user }, context_instance=RequestContext(request) )


def create_event(request):
  if (request.POST):
    f=EventForm(request.POST)
    new_Event=f.save(commit=False)
    new_Event.host=request.user.get_profile()
    new_Event.save()
    print vars(new_Event)
    return redirect('event_detail', slug=new_Event.id )
  
  else:  
    return render_to_response('create_event.html', {'form':EventForm()},context_instance=RequestContext(request) )

def event_detail(request, slug):
  print slug
  event = Event.objects.get(id=slug)

  return render_to_response('event_detail.html', {'event':event},context_instance=RequestContext(request) )
