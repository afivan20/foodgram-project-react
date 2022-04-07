from django.contrib import admin
from users.models import User, Follow


class UserAdmin(admin.ModelAdmin):
    list_display = ("pk", "email", "full_name", "is_superuser", "is_active")
    list_filter = ("email", "username")

    def save_model(self, request, obj, form, change):
        if obj.pk:
            orig_obj = User.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        obj.save()


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "author",
    )


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
