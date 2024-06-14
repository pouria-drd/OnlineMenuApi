from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.exceptions import PermissionDenied

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from menus.models import Menu
from products.models import Product
from categories.models import Category
from products.serializers import ProductSerializer
from categories.serializers import CategorySerializer


class CategoryListCreateAPIView(ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated | IsAdminUser]

    def post(self, request: Request, *args, **kwargs):
        try:
            menu_slug = kwargs.get("menu_slug")
            menu = Menu.objects.get(slug=menu_slug, is_active=True)

            # Ensure only owners or admins can create categories
            if not (request.user == menu.owner or request.user.is_superuser):
                return Response(
                    {
                        "detail": _(
                            "You do not have permission to create new category for this menu."
                        )
                    },
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

            # Check if the requesting user is the owner or an admin
            if self.request.user == menu.owner or self.request.user.is_superuser:
                # Retrieve categories related to the active menu
                return Category.objects.filter(menu=menu, is_active=True)

            else:
                raise PermissionDenied(
                    {"detail": _("You do not have permission to access this menu.")}
                )

        except Menu.DoesNotExist:
            # If the menu with the specified slug does not exist
            return Category.objects.none()


class CategoryDetailUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response(
                {"detail": _("Category not found for this menu.")},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request: Request, *args, **kwargs):
        try:
            menu_slug = kwargs.get("menu_slug")
            menu = Menu.objects.get(slug=menu_slug, is_active=True)
            category_id = kwargs.get("category_id")

            category = Category.objects.get(id=category_id, menu=menu)

            if not (request.user == menu.owner or request.user.is_superuser):
                return Response(
                    {"detail": _("You do not have permission to perform this action.")},
                    status=status.HTTP_403_FORBIDDEN,
                )

            serializer = self.get_serializer(category, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)

        except Menu.DoesNotExist:
            return Response(
                {"detail": _("Menu does not exist or is not active.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Category.DoesNotExist:
            return Response(
                {"detail": _("Category not found for this menu.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        except ValidationError as e:
            return Response(
                {"detail": _(str(e))},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get_queryset(self):
        menu_slug = self.kwargs.get("menu_slug")

        try:
            menu = Menu.objects.get(slug=menu_slug, is_active=True)
            return Category.objects.filter(menu=menu)

        except Menu.DoesNotExist:
            return Category.objects.none()

    def get_object(self):
        queryset = self.get_queryset()
        category_id = self.kwargs.get("category_id")

        try:
            return queryset.get(id=category_id)
        except Category.DoesNotExist:
            return None


class ProductListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs):
        try:
            category_id = self.kwargs.get("category_id")
            category = Category.objects.get(id=category_id, is_active=True)

            if not (request.user == category.menu.owner or request.user.is_superuser):
                return Response(
                    {"detail": "You do not have permission to perform this action."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(category=category)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Category.DoesNotExist:
            return Response(
                {"detail": _("Category does not exist or is not active.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        except ValidationError as e:
            return Response(
                {"detail": _(str(e))},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def list(self, request: Request, *args, **kwargs):
        # Retrieve queryset of products
        queryset = self.get_queryset()
        if queryset.exists():
            # Serialize and return products if queryset is not empty
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        else:
            # Return custom response when no products are found
            return Response(
                {"detail": _("No products found for this category.")},
                status=status.HTTP_404_NOT_FOUND,
            )

    def get_queryset(self):
        """
        Retrieve products belonging to an active category specified by 'category_id'.
        Filter categories that are also active.
        """

        category_id = self.kwargs.get("category_id")

        try:
            # Attempt to retrieve the category with the given id
            category = Category.objects.get(id=category_id, is_active=True)
            # Retrieve products related to the active category
            return Product.objects.filter(category=category, is_active=True)

        except Category.DoesNotExist:
            # If the menu with the specified slug does not exist
            return Product.objects.none()


class ProductDetailUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response(
                {"detail": _("Product not found for this category.")},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request: Request, *args, **kwargs):
        try:
            instance = self.get_object()
            category_id = self.kwargs.get("category_id")
            category = Category.objects.get(id=category_id, is_active=True)

            if not (request.user == category.menu.owner or request.user.is_superuser):
                return Response(
                    {"detail": "You do not have permission to perform this action."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(category=category)

            return Response(serializer.data)

        except Category.DoesNotExist:
            return Response(
                {"detail": _("Category does not exist or is not active.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Product.DoesNotExist:
            return Response(
                {"detail": _("Product not found for this menu.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        except ValidationError as e:
            return Response(
                {"detail": _(str(e))},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")

        try:
            category = Category.objects.get(id=category_id, is_active=True)
            return Product.objects.filter(category=category, is_active=True)
        except Category.DoesNotExist:
            return Product.objects.none()

    def get_object(self):
        queryset = self.get_queryset()
        product_id = self.kwargs.get("product_id")

        try:
            return queryset.get(id=product_id)
        except Product.DoesNotExist:
            return None
