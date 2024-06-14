from categories.models import Category
from rest_framework import serializers
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "menu",
            "name",
            "slug",
            "icon",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        # Ensure that the 'name' field is unique within the same menu
        menu = attrs.get("menu")
        name = attrs.get("name")

        if Category.objects.filter(menu=menu, name=name).exists():
            raise serializers.ValidationError(
                {
                    "detail": _("Category with this name already exists in the menu."),
                }
            )

        return attrs

    def create(self, validated_data):
        if not validated_data.get("slug"):
            validated_data["slug"] = slugify(validated_data["name"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if not validated_data.get("slug"):
            validated_data["slug"] = slugify(validated_data.get("name", instance.name))
        return super().update(instance, validated_data)
