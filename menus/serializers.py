from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from products.models import Product
from categories.models import Category


class CustomerProductSerializer(ModelSerializer):
    icon = SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "price",
            "icon",
        )

        # All fields are read-only
        read_only_fields = ["__all__"]

    def get_icon(self, obj):
        """
        Custom method to retrieve the absolute URL of the category's icon.
        Uses request context to build the URL if the icon exists.
        """
        request = self.context.get("request")
        if obj.icon:
            return request.build_absolute_uri(obj.icon.url)
        return None


class CustomerCategoryDetailSerializer(ModelSerializer):
    products = CustomerProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "icon",
            "products",
        )

        # All fields are read-only
        read_only_fields = ["__all__"]

    def get_icon(self, obj):
        """
        Custom method to retrieve the absolute URL of the category's icon.
        Uses request context to build the URL if the icon exists.
        """
        request = self.context.get("request")
        if obj.icon:
            return request.build_absolute_uri(obj.icon.url)
        return None


class CustomerCategorySerializer(ModelSerializer):
    icon = SerializerMethodField()

    class Meta:
        model = Category

        fields = (
            "id",
            "name",
            "icon",
        )

        # All fields are read-only
        read_only_fields = ["__all__"]

    def get_icon(self, obj):
        """
        Custom method to retrieve the absolute URL of the category's icon.
        Uses request context to build the URL if the icon exists.
        """
        request = self.context.get("request")
        if obj.icon:
            return request.build_absolute_uri(obj.icon.url)
        return None
