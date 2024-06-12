from menu.models import Menu
from django.contrib import admin


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "owner",
        "slug",
        "is_active",
        "created_at",
        "updated_at",
    ]

    prepopulated_fields = {"slug": ("name",)}
    actions = ["set_menus_inactive", "set_menus_active"]
    list_filter = ["is_active", "created_at", "updated_at"]
    search_fields = ["name", "owner__username", "address", "slug"]

    @admin.action(description="Set selected menus as inactive")
    def set_menus_inactive(self, request, queryset):
        updated_count = queryset.update(is_active=False)
        self.message_user(
            request, f"{updated_count} menus were successfully marked as inactive."
        )

    @admin.action(description="Set selected menus as active")
    def set_menus_active(self, request, queryset):
        updated_count = queryset.update(is_active=True)
        self.message_user(
            request, f"{updated_count} menus were successfully marked as active."
        )
