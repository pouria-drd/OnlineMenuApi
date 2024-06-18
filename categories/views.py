from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from django.utils.translation import gettext_lazy as _

from menus.models import Menu
from categories.models import Category
from categories.serializers import CategorySerializer


class CategoryListCreateAPIView(ListCreateAPIView):
    """
    API view to list and create categories for a menu.

    - Requires authentication.
    - GET: List all categories for the authenticated user's active menu.
    - POST: Create a new category for the authenticated user's menu.
    """

    allowed_methods = ["GET", "POST"]
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def list(self, request: Request, *args, **kwargs):
        """
        List all active categories for the authenticated user's active menu.

        - Returns a 404 response if no active menu or categories are found.
        """

        queryset = self.get_queryset()
        # Serialize and return the queryset data
        if queryset.exists():
            menu_name = Menu.objects.get(owner=request.user).name
            serializer = self.serializer_class(
                queryset, context={"request": request}, many=True
            )
            return Response({"menuName": menu_name, "categories": serializer.data})

        else:
            # Handle case where no categories are found
            return Response(
                {"detail": _("No categories found for this user or menu.")},
                status=status.HTTP_404_NOT_FOUND,
            )

    def post(self, request):
        """
        Create a new category for the authenticated user's menu.

        - Requires the user to have an active menu.
        - Validates the category data using the serializer.
        - Returns the created category data on success.
        """
        try:
            # Retrieve the menu associated with the authenticated user
            request_user = request.user
            menu = Menu.objects.get(owner=request_user, is_active=True)

            # Serialize and validate the incoming data
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Save the new category with the associated menu
            serializer.save(menu=menu)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Menu.DoesNotExist:
            # Handle case where the user does not have an associated menu
            return Response(
                {"detail": _("Menu not found!")},
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

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        # Ensure the request object is passed to the serializer context
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        """
        Retrieve the queryset of active categories for the authenticated user's active menu.

        - Returns an empty queryset if no active menu is found.
        """
        try:
            # Get the authenticated user from the request
            request_user = self.request.user
            # Retrieve the active menu associated with the authenticated user
            menu = Menu.objects.get(owner=request_user, is_active=True)

            # Filter categories that are active and associated with the menu
            categories = Category.objects.filter(menu=menu)
            return categories

        except Menu.DoesNotExist:
            # Return an empty queryset if no active menu is found
            return Category.objects.none()


class CategoryDetailUpdateAPIView(RetrieveUpdateAPIView):
    """
    API view to retrieve and update details of a specific category.

    - Requires authentication.
    - GET: Retrieve details of an existing category.
    - PUT/PATCH: Update details of an existing category associated with the authenticated user's active menu.
    """

    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ["GET", "PATCH", "PUT"]

    def retrieve(self, request: Request, *args, **kwargs):
        """
        GET method to retrieve details of an existing category.

        - Retrieves the category instance using get_object().
        - Returns serialized category data or a 404 response if category is not found.
        """
        # Get the category instance
        instance = self.get_object()

        # Return 404 error if category is not found
        if instance is None:
            return Response(
                {"detail": _("Category not found!")},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize and return the category data
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request: Request, *args, **kwargs):
        """
        PUT/PATCH method to update details of an existing category.

        - Retrieves the authenticated user and associated active menu.
        - Retrieves the category ID from URL parameters.
        - Retrieves the existing category object.
        - Validates and saves the updated category data using the serializer.
        - Returns the updated category data or appropriate error responses.
        """
        try:
            # Get the authenticated user and associated active menu
            request_user = request.user
            menu = Menu.objects.get(owner=request_user, is_active=True)

            # Get the category with ID from URL parameters
            category_id = self.kwargs.get("category_id")
            category = Category.objects.get(menu=menu, id=category_id)

            # Deserialize and validate the incoming data
            serializer = self.get_serializer(category, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            # Save and return the updated category
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
        Retrieve the category instance based on the provided category ID.
        """
        # Get the queryset of categories
        queryset = self.get_queryset()
        # Get the category ID from URL parameters
        category_id = self.kwargs.get("category_id")

        try:
            # Return the category instance
            return queryset.get(id=category_id)
        # Return None if category is not found
        except Category.DoesNotExist:
            return None

    def get_queryset(self):
        """
        Retrieve the queryset of categories for the authenticated user's active menu.

        If the active menu does not exist, returns an empty queryset.
        """
        try:
            # Get the authenticated user and associated active menu
            request_user = self.request.user
            menu = Menu.objects.get(owner=request_user, is_active=True)

            # Get all active categories for the menu
            categories = Category.objects.filter(menu=menu)
            return categories
        # Return an empty queryset if menu is not found
        except Menu.DoesNotExist:
            return Category.objects.none()
