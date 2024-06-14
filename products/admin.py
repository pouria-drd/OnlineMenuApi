from django.contrib import admin
from django.utils.html import format_html

from products.models import Product
from categories.models import Category
from categories.admin import CategoryAdmin


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "price",
        "category",
        "is_active",
        "icon_display",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "slug", "category__name", "slug")
    list_filter = ("is_active", "created_at", "updated_at")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["created_at", "updated_at"]

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
        self.message_user(request, f"Successfully activated {updated} products.")

    make_active.short_description = "Activate selected products"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"Successfully deactivated {updated} products.")

    make_inactive.short_description = "Deactivate selected products"


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    readonly_fields = ("created_at", "updated_at")
    fields = ("name", "price", "slug", "icon", "is_active")
    show_change_link = True


class CategoryAdminWithProducts(CategoryAdmin):
    inlines = [ProductInline]


# Unregister the default Category admin and register the custom one with the inline.
admin.site.unregister(Category)
admin.site.register(Category, CategoryAdminWithProducts)
