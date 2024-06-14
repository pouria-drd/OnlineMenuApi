from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "phone_number")},
        ),
        ("Additional info", {"fields": ("user_type",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    # "user_type",
                    # "phone_number",
                    # "first_name",
                    # "last_name",
                    # "email",
                    # "is_active",
                    # "is_staff",
                    # "is_superuser",
                    # "groups",
                    # "user_permissions",
                ),
            },
        ),
        ("Optional", {"classes": ("wide",), "fields": ("email", "phone_number")}),
    )

    list_display = [
        "username",
        "full_name",
        "user_type",
        "phone_number",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
        "date_joined",
        "updated_at",
    ]

    search_fields = ["username", "email", "phone_number", "first_name", "last_name"]
    ordering = ["-date_joined"]

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_add_fieldsets(self, request):
        return self.add_fieldsets
