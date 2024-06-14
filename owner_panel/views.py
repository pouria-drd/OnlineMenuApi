from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from menus.models import Menu
from categories.models import Category
from categories.serializers import CategorySerializer


class CategoryCreateAPIView(ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated | IsAdminUser]

    def list(self, request: Request, *args, **kwargs):
        # Retrieve queryset of categories
        queryset = self.get_queryset()

        if queryset.exists():
            # Serialize and return categories if queryset is not empty
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        else:
            # Return custom response when no categories are found
            return Response(
                {"detail": _("No categories found for this menu.")},
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

    def post(self, request: Request, *args, **kwargs):
        try:
            menu_slug = kwargs.get("menu_slug")
            menu = Menu.objects.get(slug=menu_slug, is_active=True)

            # Ensure only owners or admins can create categories
            if not (request.user == menu.owner or request.user.is_superuser):
                return Response(
                    {"detail": _("You do not have permission to perform this action.")},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Serialize incoming data and validate
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Save the category with the associated menu
            serializer.save(menu=menu)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Menu.DoesNotExist:
            return Response(
                {"detail": _("Menu does not exist or is not active.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        except ValidationError as e:
            return Response(
                {"detail": _(str(e))},
                status=status.HTTP_400_BAD_REQUEST,
            )
