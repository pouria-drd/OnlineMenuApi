from categories.models import Category
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class CustomerMenuCategorySerializer(ModelSerializer):
    icon = SerializerMethodField()

    class Meta:
        model = Category

        fields = (
            "name",
            "slug",
            "icon",
        )

        # All fields are read-only
        read_only_fields = ["__all__"]

        # Human-readable label for name, slug and icon
        extra_kwargs = {
            "name": {"label": _("Name")},
            "slug": {"label": _("Slug")},
            "icon": {"label": _("Icon")},
        }

    def get_icon(self, obj):
        """
        Custom method to retrieve the absolute URL of the category's icon.
        Uses request context to build the URL if the icon exists.
        """
        request = self.context.get("request")
        if obj.icon:
            return request.build_absolute_uri(obj.icon.url)
        return None
