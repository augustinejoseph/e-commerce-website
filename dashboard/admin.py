from django.contrib import admin
from accounts.models import Account
from accounts.models import UserProfile
from django.utils.html import format_html

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html(
            '<img src ="{}" width="30px" style="border-radius:50%;">'.format(
                object.profile_picture.url
            )
        )

    thumbnail.short_description = "prof ile picture"
    list_display = (
        "thumbnail",
        "user",
        "city",
        "state",
    )
