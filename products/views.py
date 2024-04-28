from rest_framework import viewsets
from django.utils.text import slugify

from products.models import Product, ProductPrice
from products.serializers import ProductSerializer, ProductPriceSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_update(self, serializer):
        instance = serializer.instance

        slug = self.request.data.get("slug")

        old_name = instance.name
        new_name = self.request.data.get("name")

        if new_name != old_name and (not slug or slug != new_name):
            serializer.validated_data["slug"] = slugify(new_name)

        serializer.save()


class ProductPriceViewSet(viewsets.ModelViewSet):
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer
