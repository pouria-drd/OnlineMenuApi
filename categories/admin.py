from django.contrib import admin
from categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "menu",
        "is_active",
        "created_at",
        "updated_at",
    ]
    list_filter = ["menu", "is_active", "created_at", "updated_at"]
    search_fields = ["name", "slug", "menu"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["created_at", "updated_at"]
    autocomplete_fields = [
        "menu"
    ]  # Allows selecting menu from a dropdown instead of a text field

    fieldsets = (
        (None, {"fields": ("menu", "name", "description", "slug")}),
        ("Status", {"fields": ("is_active",)}),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    actions = ["activate_categories", "deactivate_categories"]

    def activate_categories(self, request, queryset):
        queryset.update(is_active=True)

    activate_categories.short_description = "Activate selected categories"

    def deactivate_categories(self, request, queryset):
        queryset.update(is_active=False)

    deactivate_categories.short_description = "Deactivate selected categories"
