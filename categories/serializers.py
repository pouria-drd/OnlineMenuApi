from categories.models import Category

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class CategorySerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "menu",
            "name",
            "icon",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = ["id", "menu", "created_at", "updated_at"]

    def validate_icon(self, value):
        if value:
            # Set the size limit to 1MB (1 * 1024 * 1024 bytes)
            size_limit = 1 * 1024 * 1024

            if value.size > size_limit:
                raise serializers.ValidationError(_("Icon size should not exceed 1MB."))

            return value
