from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from menus.models import Menu
from categories.models import Category
from categories.serializers import CustomerMenuCategorySerializer


class CustomerMenuCategoryListView(ListAPIView):
    permission_classes = [AllowAny]  # Allow access to anyone (public view)
    serializer_class = CustomerMenuCategorySerializer

    def get_queryset(self):
        """
        Retrieve categories belonging to an active menu specified by 'menu_slug'.
        Filter categories that are also active.
        """

        menu_slug = self.kwargs.get("menu_slug")

        try:
            menu = Menu.objects.get(slug=menu_slug, is_active=True)
            return Category.objects.filter(menu=menu, is_active=True)

        except Menu.DoesNotExist:
            return Category.objects.none()
