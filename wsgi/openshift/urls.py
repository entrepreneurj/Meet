from django.conf.urls.defaults import patterns, include, url
from django.core.urlresolvers import reverse

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from meet.views import UserProfileDetailView, dashboard, home, friends, create_event, event_detail, event_edit, profile, profile_edit, profile_events
from api.views import get_friends
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'openshift.views.home', name="home"),
    url(r'^$', home, name="home"),
    # url(r'^openshift/', include('openshift.foo.urls')),
#    url(r'^i$', 'meet.views.accountform', name='accountform'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r"^login/$", "django.contrib.auth.views.login",
      {"template_name": "login.html"}, name="login"),
    url(r"^logout/$", "django.contrib.auth.views.logout_then_login", name="logout"),
    # Uncomment the next line to enable the admin:

    #url(r'^users/(?P<slug>\w+)/$', UserProfileDetailView.as_view(), name="profile"), 
    url(r'^users/(?P<slug>\w+)/$', profile, name="profile"), 
    url(r'^users/(?P<slug>\w+)/edit/$', profile_edit, name="profile_edit"), 
    url(r'^users/(?P<slug>\w+)/events/$', profile_events, name="profile_events"), 
    url(r'^dashboard/$', dashboard, name="dashboard"), 
    url(r'^users/(?P<slug>\w+)/friends/$', friends, name="friends"), 
    url(r'^events/create/$', create_event, name="create_event"), 
    url(r'^events/(?P<slug>\d+)/$', event_detail, name="event_detail"), 
    url(r'^events/(?P<slug>\d+)/edit/$', event_edit, name="event_edit"), 

    #### API #####    
    url(r'^api/friends/$', get_friends, name="get_friends"), 
    
    
    
    url(r'^admin/', include(admin.site.urls)),


)
