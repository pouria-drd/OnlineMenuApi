from rest_framework import serializers
from products.models import Product, ProductPrice


class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ["id", "price", "user", "product", "created_at"]


class ProductSerializer(serializers.ModelSerializer):
    prices = ProductPriceSerializer(many=True, read_only=True)

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
            "prices",
        ]
