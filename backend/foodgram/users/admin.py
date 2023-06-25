from django.conf import settings
from django.contrib import admin

from users.models import Subscription, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("pk", "email", "username", "first_name", "last_name")
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ("username", "email")
    empty_value_display = settings.EMPTY_VALUE


    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "author")
    search_fields = ("user", "author")
    list_filter = ("user", "author")
    empty_value_display = settings.EMPTY_VALUE
