from django.contrib import admin
from .models import Account, UserProfile, Address
from django.utils.html import format_html


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html(
            '<img src ="{}" width="30px" style="border-radius:50%;">'.format(
                object.profile_picture.url
            )
        )

    thumbnail.short_description = "profile picture"
    list_display = (
        "thumbnail",
        "user",
        "city",
        "state",
    )


class AddressManager(admin.ModelAdmin):
    list_display = (
        "account",
        "firstName",
        "lastName",
        "email",
        "phone",
        "addressLineOne",
        "addressLineTwo",
    )


admin.site.register(Account)
admin.site.register(Address, AddressManager)
admin.site.register(UserProfile, UserProfileAdmin)
