# Create your views here.
from django.core.context_processors import csrf
from meet.models import *
from django.shortcuts import render
from django.views.generic import DetailView
#Django 1.5 from django.contrib.auth import get_user_model
from django.contrib.auth.models import User #Django < 1.5


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
