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


class ProductDetailUpdateAPIView(RetrieveUpdateAPIView):
    """
    API view to retrieve and update a specific product within a category.

    - Requires authentication.
    - GET: Retrieve details of an existing product.
    - PUT/PATCH: Update an existing product under a specific category for the authenticated user's active menu.
    """

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ["GET", "PATCH", "PUT"]

    def retrieve(self, request: Request, *args, **kwargs):
        """
        GET method to retrieve details of an existing product.

        - Retrieves the product instance using get_object().
        - Returns serialized product data or a 404 response if product is not found.
        """
        # Get the product instance
        instance = self.get_object()

        # Return 404 error if product is not found
        if instance is None:
            return Response(
                {"detail": _("Product not found!")},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize and return the product data
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request: Request, *args, **kwargs):
        """
        PUT/PATCH method to update an existing product.

        - Retrieves the authenticated user and associated active menu.
        - Retrieves the category and product IDs from URL parameters.
        - Retrieves the existing product object.
        - Validates and saves the updated product data using the serializer.
        - Returns the updated product data or appropriate error responses.
        """
        try:
            # Get the authenticated user and associated active menu
            request_user = request.user
            menu = Menu.objects.get(owner=request_user, is_active=True)

            # Get the category with ID from URL parameters
            category_id = self.kwargs.get("category_id")
            category = Category.objects.get(menu=menu, id=category_id, is_active=True)

            # Get the product with ID from URL parameters
            product_id = self.kwargs.get("product_id")
            product = Product.objects.get(category=category, id=product_id)

            # Deserialize and validate the incoming data
            serializer = self.get_serializer(product, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            # Save and return the updated product
            serializer.save()
            return Response(serializer.data)

        except Menu.DoesNotExist:
            # Return 404 error if menu is not found
            return Response(
                {"detail": _("Menu not found!")},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Category.DoesNotExist:
            # Return 404 error if category is not found
            return Response(
                {"detail": _("Category not found!")},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Product.DoesNotExist:
            # Return 404 error if product is not found
            return Response(
                {"detail": _("Product not found!")},
                status=status.HTTP_404_NOT_FOUND,
            )

        except ValidationError as e:
            # Return 400 error if data is invalid
            return Response(
                {"detail": _("Invalid Data!")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            # Print the exception and return 400 error for any other issues
            # print(str(e))
            return Response(
                {"detail": _("Something went wrong!")},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get_object(self):
        """
        Retrieve the product instance based on the URL parameters.

        - Retrieves the queryset of categories using get_queryset().
        - Retrieves the product ID from URL parameters.
        - Returns the product instance if found; otherwise, returns None.
        """
        # Get the queryset of categories
        queryset = self.get_queryset()
        # Get the product ID from URL parameters
        product_id = self.kwargs.get("product_id")

        try:
            return queryset.get(id=product_id)
        # Return None if category is not found
        except Category.DoesNotExist:
            return None
        # Return None if product is not found
        except Product.DoesNotExist:
            return None

    def get_queryset(self):
        """
        Retrieve the queryset of products filtered by category and menu.

        - Retrieves the authenticated user from the request.
        - Retrieves the associated active menu.
        - Retrieves the category ID from URL parameters.
        - Returns the queryset of products filtered by category and menu.
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
