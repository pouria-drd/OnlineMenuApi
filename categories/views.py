from rest_framework import viewsets
from django.utils.text import slugify

from categories.models import Category
from categories.serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def perform_update(self, serializer):
        instance = serializer.instance

        slug = self.request.data.get("slug")

        old_name = instance.name
        new_name = self.request.data.get("name")

        if new_name != old_name and (not slug or slug != new_name):
            serializer.validated_data["slug"] = slugify(new_name)

        serializer.save()
