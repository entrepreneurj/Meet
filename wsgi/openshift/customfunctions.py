#from django.db import models
#from django import forms
#from django.db.models.signals import post_save
#from django.contrib.auth.models import User
from datetime import datetime
#from django.utils import timezone
#from gettext import gettext as _

EPOCH=1375723412

# invite functions


def get_timestamp_from_datetime(dt):
  timestamp=dt.strftime("%s")
  return int(timestamp)-EPOCH

def get_timestamp_from_unix_timestamp(ts):
  return ts-EPOCH

def get_current_timestamp():
  now=datetime.now()
  ts=get_timestamp_from_datetime(now)
  return ts
