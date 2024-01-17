from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'first_name', 'last_name', 'referred_by')
    list_filter = ('first_name', 'last_name', 'phone_number')
