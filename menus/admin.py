from menus.models import Menu
from django.contrib import admin


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "is_active", "created_at", "updated_at"]
    list_filter = ["is_active", "created_at", "updated_at"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (None, {"fields": ("name", "description", "slug")}),
        ("Status", {"fields": ("is_active",)}),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    actions = ["activate_menus", "deactivate_menus"]

    def activate_menus(self, request, queryset):
        queryset.update(is_active=True)

    activate_menus.short_description = "Activate selected menus"

    def deactivate_menus(self, request, queryset):
        queryset.update(is_active=False)

    deactivate_menus.short_description = "Deactivate selected menus"
