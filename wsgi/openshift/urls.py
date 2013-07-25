from django.conf.urls.defaults import patterns, include, url
from django.core.urlresolvers import reverse

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from meet.views import UserProfileDetailView, dashboard

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'openshift.views.home', name="home"),
    # url(r'^openshift/', include('openshift.foo.urls')),
#    url(r'^i$', 'meet.views.accountform', name='accountform'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r"^login/$", "django.contrib.auth.views.login",
      {"template_name": "login.html"}, name="login"),
    url(r"^logout/$", "django.contrib.auth.views.logout_then_login", name="logout"),
    # Uncomment the next line to enable the admin:

    url(r'^users/(?P<slug>\w+)/$', UserProfileDetailView.as_view(), name="profile"), 
    url(r'^dashboard/$', dashboard, name="dashboard"), 

    
    url(r'^admin/', include(admin.site.urls)),


)
