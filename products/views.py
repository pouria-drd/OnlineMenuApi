from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from django.utils.translation import gettext_lazy as _

from menus.models import Menu
from products.models import Product
from categories.models import Category
from products.serializers import ProductSerializer


class ProductListCreateAPIView(ListCreateAPIView):
    """
    API view for listing and creating products within a specific category.

    - Requires authentication.
    - GET: List all products for a specific category under the authenticated user's active menu.
    - POST: Create a new product under a specific category for the authenticated user's active menu.
    """

    allowed_methods = ["GET", "POST"]
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request: Request, *args, **kwargs):
        """
        GET method to list all products for a specific category.

        - Retrieves the category ID from URL kwargs.
        - Retrieves the associated menu and category objects.
        - Returns serialized product data or a 404 response if no products are found.
        """

        queryset = self.get_queryset()
        # Serialize and return the queryset data
        if queryset.exists():
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)

        else:
            # Handle case where no products are found
            return Response(
                {"detail": _("No products found for this category.")},
                status=status.HTTP_404_NOT_FOUND,
            )

    def post(self, request: Request, *args, **kwargs):
        """
        POST method to create a new product under a specific category.

        - Retrieves the category ID from URL kwargs.
        - Retrieves the associated menu and category objects.
        - Validates and saves the incoming product data using the serializer.
        - Returns the created product data or appropriate error responses.
        """
        try:
            # Retrieve the menu associated with the authenticated user
            request_user = request.user
            menu = Menu.objects.get(owner=request_user, is_active=True)

            category_id = self.kwargs.get("category_id")
            category = Category.objects.get(menu=menu, id=category_id, is_active=True)

            # Serialize and validate the incoming data
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Save the new product with the associated category
            serializer.save(category=category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Menu.DoesNotExist:
            # Handle case where the user does not have an associated menu
            return Response(
                {"detail": _("Menu not found!")},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Category.DoesNotExist:
            # Handle case where the menu does not have an associated category
            return Response(
                {"detail": _("Category not found!")},
                status=status.HTTP_404_NOT_FOUND,
            )

        except ValidationError as ve:
            # Handle validation errors raised by the serializer
            return Response(
                {"detail": _("Invalid Data!")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            # Handle any other unexpected exceptions
            print(str(e))
            return Response(
                {"detail": _("Something went wrong...")},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_queryset(self):
        """
        Retrieves the queryset of products for a specific category.

        - Retrieves the authenticated user from the request.
        - Retrieves the associated menu and category objects based on URL kwargs.
        - Returns active products associated with the category or empty queryset if not found.
        """
        try:
            # Retrieve the authenticated user from the request
            request_user = self.request.user
            # Retrieve the menu associated with the authenticated user
            menu = Menu.objects.get(owner=request_user, is_active=True)

            # Retrieve category_id from URL kwargs
            category_id = self.kwargs.get("category_id")
            # Retrieve the category object associated with the menu and category_id
            category = Category.objects.get(menu=menu, id=category_id, is_active=True)

            # Filter products that are active and associated with the category
            products = Product.objects.filter(category=category, is_active=True)

            return products

        except Menu.DoesNotExist:
            # Return an empty queryset if no active menu is found
            return Category.objects.none()

        except Category.DoesNotExist:
            # Return an empty queryset if no active category is found
            return Product.objects.none()
