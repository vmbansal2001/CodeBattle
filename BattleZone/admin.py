from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from BattleZone.models import PersonalInfo2

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class PersonalInfo2Inline(admin.StackedInline):
    model = PersonalInfo2
    can_delete = False
    verbose_name_plural = 'PersonalInfo2'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (PersonalInfo2Inline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
