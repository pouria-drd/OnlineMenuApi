from products.models import Product
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class ProductSerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "name",
            "price",
            "icon",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = ["id", "category", "created_at", "updated_at"]
