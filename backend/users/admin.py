from django.contrib import admin
from users.models import User, Follow
from django.contrib.auth.admin import UserAdmin


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "author",
    )


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
