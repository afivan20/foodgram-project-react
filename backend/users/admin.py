from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'username', 'first_name', 'last_name', 'role')
    list_filter = ('email', 'username')

admin.site.register(User, UserAdmin)
