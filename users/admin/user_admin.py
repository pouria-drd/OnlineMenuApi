from django.contrib import admin
from users.models import UserModel
from django.contrib.auth.admin import UserAdmin


@admin.register(UserModel)
class UserAdmin(UserAdmin):
    model = UserModel

    list_display = [
        "username",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
        "created_at",  # Remove updated_at since it's non-editable
    ]
    search_fields = ["username", "first_name", "last_name", "email", "phone_number"]
    ordering = [
        "username",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "is_active",
        "is_staff",
        "is_superuser",
    ]

    readonly_fields = ["id", "last_login", "updated_at", "created_at"]

    # Fields to be displayed on the user admin page
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "phone_number", "email")},
        ),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser", "user_permissions")},
        ),
        (
            "Important dates",
            {"fields": ("last_login", "created_at")},
        ),  # Remove updated_at
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "phone_number",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
