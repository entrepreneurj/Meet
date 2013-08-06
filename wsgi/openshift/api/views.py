# Create your views here.
from meet.models import *
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.utils import simplejson
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
#from django.utils.decorators import method_decorator
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import get_template
from django.template import Context
import uuid
from customfunctions import *
from django.contrib.sites.models import Site

def get_user_from_session(session_key):
  #Thanks to http://scottbarnham.com/blog/2008/12/04/get-user-from-session-key-in-django/
  session = Session.objects.get(session_key=session_key)
  uid = session.get_decoded().get('_auth_user_id')
  user = User.objects.get(pk=uid)
  return user

def event_invite(uname, event):
  invite=Attendee()
  invite.usr_profile=UserProfile.objects.get(user__username=uname);
  invite.event=event
  invite.save()
  #print invite
  return None


def invite_event_email(usr_profile, email_add, event):
  invite_id=str(uuid.uuid4())
  plaintext = get_template('registration/new_user.txt')
  invite=UserInvite()
  invite.request_id=invite_id
  invite.email_address=email_add
  invite.invited_by=usr_profile
  invite.event_invite=event
  invite.save()
  invite_link='/'.join([str(invite.invite_date),str(invite_id),])
  htmly     = get_template('registration/new_user.html')
  d = Context({ 'usr_profile': usr_profile , 'uuid': invite_link, 'site':Site.objects.get_current().domain})
  subject= ''.join(['[MeetApp] An invite from ', usr_profile.user.get_full_name(),])
  from_email, to = 'joe.letts@me.com', email_add
  text_content = plaintext.render(d)
  html_content = htmly.render(d)
  msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
  msg.attach_alternative(html_content, "text/html")
  msg.send(fail_silently=False)
  #usr=User()\
  return None

#@method_decorator(csrf_exempt)
def get_friends(request):
  friends_json=[]
  user=request.user;
  usr_profile, created =UserProfile.objects.get_or_create(user=user)
    #friends=UserProfile.get_friends(usr_profile);
  event=Event.objects.get(pk=request.POST.get("event_id",'')  );
  #print (vars(event))
  if ( (request.POST.get("action",'')=="invite")  ):
    invitee_list=simplejson.loads (request.POST.get("list",'') );
    for member in invitee_list:
      #   print member, member[1]
      if (member[1]=="1"):
        event_invite(member[0],event)
  if ( request.POST.get("action",'')=="friends"  ):
    friends=UserProfile.objects.filter(relationship__friend=usr_profile)
    friends=friends.exclude(attendee__in=event.attendee_set.all())
    
    for friend in friends:
      friend_data={'u': friend.user.username, 'n':friend.user.get_full_name(), 'p':friend.get_picture() }
      friends_json.append(friend_data)
     
    return HttpResponse(simplejson.dumps(friends_json), mimetype='application/json')
  else:
    friends_json.append("error")
    return HttpResponse(simplejson.dumps(friends_json), mimetype='application/json')


def invite(request):
  user_profile, created=UserProfile.objects.get_or_create(user=request.user);
  friends_json=[]
  event=Event.objects.get(pk=request.POST.get("event_id",'')  );
  if ( (request.POST.get("action",'')=="user-invite")   ):
    invitee_list=simplejson.loads (request.POST.get("email_list",'') )
    print invitee_list
    for email_msg in invitee_list:
      invite_event_email(user_profile,email_msg, event)
    friends_json.append("request received")
  else:
    friends_json.append("error")
  print friends_json
  return HttpResponse(simplejson.dumps(friends_json), mimetype='application/json')
    
