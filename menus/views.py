from rest_framework import viewsets
from django.utils.text import slugify

from menus.models import Menu
from menus.serializers import MenuSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def perform_update(self, serializer):
        instance = serializer.instance

        slug = self.request.data.get("slug")

        old_name = instance.name
        new_name = self.request.data.get("name")

        if new_name != old_name and (not slug or slug != new_name):
            serializer.validated_data["slug"] = slugify(new_name)

        serializer.save()
