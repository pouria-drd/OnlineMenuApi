from category.models import Category

from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ModelSerializer


class CustomerCategorySerializer(ModelSerializer):

    class Meta:
        model = Category

        fields = (
            "name",
            "slug",
            "icon",
        )

        read_only_fields = ["__all__"]

        extra_kwargs = {
            "name": {"label": _("Name")},
            "slug": {"label": _("Slug")},
            "icon": {"label": _("Icon")},
        }
