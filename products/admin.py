from django.contrib import admin
from products.models import Product, ProductPrice


class ProductPriceInline(admin.TabularInline):
    model = ProductPrice


@admin.register(ProductPrice)
class ProductPriceAdmin(admin.ModelAdmin):
    ordering = ["-created_at"]
    list_display = ["price", "user", "product", "created_at"]
    list_filter = ["user", "product", "created_at"]
    search_fields = ["price", "user__username", "product__name"]
    readonly_fields = ["created_at"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    ordering = ["-created_at"]
    inlines = [ProductPriceInline]

    list_display = [
        "name",
        "slug",
        "category",
        "is_active",
        "created_at",
        "updated_at",
    ]

    list_filter = ["category", "is_active", "created_at", "updated_at"]

    search_fields = ["name", "slug", "category"]

    prepopulated_fields = {"slug": ("name",)}

    readonly_fields = ["created_at", "updated_at"]

    autocomplete_fields = [
        "category"
    ]  # Allows selecting category from a dropdown instead of a text field

    fieldsets = (
        (None, {"fields": ("category", "name", "description", "slug")}),
        ("Status", {"fields": ("is_active",)}),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    actions = ["activate_products", "deactivate_products"]

    def activate_products(self, request, queryset):
        queryset.update(is_active=True)

    activate_products.short_description = "Activate selected products"

    def deactivate_products(self, request, queryset):
        queryset.update(is_active=False)

    deactivate_products.short_description = "Deactivate selected products"
