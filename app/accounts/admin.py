from django.contrib import admin

# Register your models here.
from accounts.models import User


class UserAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'email']


admin.site.register(User, UserAdmin)
