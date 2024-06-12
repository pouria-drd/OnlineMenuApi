from users.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class UserAdmin(UserAdmin):
    model = User

    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("user_type",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("user_type",)}),)

    list_display = [
        "username",
        "full_name",
        "user_type",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
        "date_joined",
        "updated_at",
    ]

    search_fields = ["username", "email", "first_name", "last_name"]

    ordering = ["username"]
