from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView, RetrieveAPIView

from django.utils.translation import gettext_lazy as _

from menus.models import Menu
from categories.models import Category

from menus.serializers import (
    CustomerCategorySerializer,
    CustomerCategoryDetailSerializer,
)


class CustomerCategoryDetailView(RetrieveAPIView):
    """
    API view to retrieve details of a specific category for public access.

    - GET: Retrieve details of a category associated with an active menu specified by 'menu_slug'.
    """

    allowed_methods = ["GET"]
    permission_classes = [AllowAny]  # Allow access to anyone (public view)
    serializer_class = CustomerCategoryDetailSerializer

    def get_queryset(self):
        """
        Retrieve queryset of categories filtered by the active menu specified by 'menu_slug'.
        """
        menu_slug = self.kwargs.get("menu_slug")

        try:
            menu = Menu.objects.get(slug=menu_slug, is_active=True)
            return Category.objects.filter(menu=menu)
        except Menu.DoesNotExist:
            return Category.objects.none()

    def get_object(self):
        """
        Retrieve the category instance based on the provided 'category_id' within the queryset.
        """
        queryset = self.get_queryset()
        category_id = self.kwargs.get("category_id")

        try:
            return queryset.get(id=category_id)
        except Category.DoesNotExist:
            return None

    def retrieve(self, request: Request, *args, **kwargs):
        """
        Handle GET request to retrieve details of a specific category.

        - Retrieves the category instance using get_object().
        - Returns serialized category data or a 404 response if category is not found.
        """
        instance = self.get_object()
        if instance is None:
            return Response(
                {"detail": _("Category not found for this menu.")},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CustomerCategoryListView(ListAPIView):
    """
    API view to retrieve a list of categories for public access.

    - GET: Retrieve a list of categories associated with an active menu specified by 'menu_slug'.
    """

    allowed_methods = ["GET"]
    permission_classes = [AllowAny]  # Allow access to anyone (public view)
    serializer_class = CustomerCategorySerializer

    def list(self, request, *args, **kwargs):
        """
        Handle GET request to retrieve a list of categories.

        - Retrieves queryset of categories using get_queryset().
        - Serializes and returns categories if queryset is not empty.
        - Returns a custom response when no categories are found.
        """

        # Retrieve queryset of categories
        queryset = self.get_queryset()

        if queryset.exists():
            # Serialize and return categories if queryset is not empty
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        else:
            # Return custom response when no categories are found
            return Response(
                {"message": "No categories found for this menu."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def get_queryset(self):
        """
        Retrieve categories belonging to an active menu specified by 'menu_slug'.
        Filter categories that are also active.
        """

        menu_slug = self.kwargs.get("menu_slug")

        try:
            # Attempt to retrieve the menu with the given slug
            menu = Menu.objects.get(slug=menu_slug, is_active=True)
            # Retrieve categories related to the active menu
            return Category.objects.filter(menu=menu, is_active=True)

        except Menu.DoesNotExist:
            # If the menu with the specified slug does not exist
            return Category.objects.none()
