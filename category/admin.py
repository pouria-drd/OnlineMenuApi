from django.contrib import admin
from django.utils.html import format_html

from menu.models import Menu
from category.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "menu",
        "is_active",
        "icon_display",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "menu__name", "slug")
    list_filter = ("is_active", "created_at", "updated_at")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")

    def icon_display(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px;" />', obj.icon.url
            )
        return ""

    icon_display.short_description = "Icon"

    actions = ["make_active", "make_inactive"]

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"Successfully activated {updated} categories.")

    make_active.short_description = "Activate selected categories"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"Successfully deactivated {updated} categories.")

    make_inactive.short_description = "Deactivate selected categories"


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0
    readonly_fields = ("created_at", "updated_at")
    fields = ("name", "slug", "icon", "is_active", "created_at", "updated_at")
    show_change_link = True


from menu.admin import MenuAdmin


class MenuAdminWithCategories(MenuAdmin):
    inlines = [CategoryInline]


# Unregister the default Menu admin and register the custom one with the inline.
admin.site.unregister(Menu)
admin.site.register(Menu, MenuAdminWithCategories)