from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from menu.models import Menu
from category.models import Category
from customer.serializers import CustomerCategorySerializer


class CustomerCategoryListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomerCategorySerializer

    def get_queryset(self):
        menu_id = self.kwargs["menu_id"]  # Extract menu id from URL
        try:
            menu = Menu.objects.get(id=menu_id, is_active=True)
            categories = Category.objects.filter(
                menu=menu, is_active=True
            )  # Filter by is_active=True
            return categories

        except Menu.DoesNotExist:
            return Category.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
