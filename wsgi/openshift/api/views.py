# Create your views here.
from meet.models import *
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.utils import simplejson
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
#from django.utils.decorators import method_decorator

def get_user_from_session(session_key):
  #Thanks to http://scottbarnham.com/blog/2008/12/04/get-user-from-session-key-in-django/
  session = Session.objects.get(session_key=session_key)
  uid = session.get_decoded().get('_auth_user_id')
  user = User.objects.get(pk=uid)
  return user

#@method_decorator(csrf_exempt)
def get_friends(request):
  friends_json=[]
  if ( (request.POST.get("action",'')=="friends")   ):
    user=request.user;
    usr_profile, created =UserProfile.objects.get_or_create(user=user)
    friends=UserProfile.get_friends(usr_profile)
    for friend in friends:
      friend_data={'u': friend.username, 'n':friend.user.get_full_name(), 'p':friend.get_picture() }
      friends_json.append(friend_data)
     
    return HttpResponse(simplejson.dumps(friends_json), mimetype='application/json')
  else:
    friends_json.append("error")
    return HttpResponse(simplejson.dumps(friends_json), mimetype='application/json')

