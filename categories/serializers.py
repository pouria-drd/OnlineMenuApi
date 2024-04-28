from rest_framework import serializers
from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "slug",
            "name",
            "menu",
            "description",
            "is_active",
            "updated_at",
            "created_at",
        ]
