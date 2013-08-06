from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
#Django 1.5 from django.contrib.auth import get_user_model
from django.contrib.auth.models import User #Django < 1.5
from meet.models import *

admin.site.register(Event)
admin.site.register(UserProfile)
admin.site.register(Attendee)
admin.site.register(Message)
admin.site.register(Event_Action)
admin.site.register(Relationship)
admin.site.register(UserInvite)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    

class UserProfileAdmin(UserAdmin):
    inlines=(UserProfileInline, )

admin.site.unregister(User)
#for Django 1.5 replace User with get_user_model()
admin.site.register(User, UserProfileAdmin)
