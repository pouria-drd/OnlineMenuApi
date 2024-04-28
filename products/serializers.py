from rest_framework import serializers
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "slug",
            "name",
            "category",
            "description",
            "is_active",
            "updated_at",
            "created_at",
        ]
