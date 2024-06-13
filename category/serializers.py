from category.models import Category

from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ModelSerializer, ValidationError


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
            "icon",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")
        extra_kwargs = {
            "name": {"label": _("Name")},
            "slug": {"label": _("Slug")},
            "icon": {"label": _("Icon")},
            "is_active": {"label": _("Is Active")},
            "created_at": {"label": _("Created At")},
            "updated_at": {"label": _("Updated At")},
        }

    def validate(self, data):
        # Ensure slug is unique within the same menu
        if Category.objects.filter(menu=data["menu"], slug=data["slug"]).exists():
            raise ValidationError(_("The slug must be unique within the same menu!"))
        return data
