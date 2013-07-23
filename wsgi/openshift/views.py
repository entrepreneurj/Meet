import os
from django.shortcuts import render_to_response

def home(request):

    host=os.environ['OPENSHIFT_MYSQL_DB_HOST'];
    return render_to_response('home/home.html', {'host':host,})
