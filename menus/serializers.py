from menus.models import Menu
from rest_framework import serializers


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            "id",
            "slug",
            "name",
            "description",
            "is_active",
            "updated_at",
            "created_at",
        ]
