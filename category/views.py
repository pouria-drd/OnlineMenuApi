from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from category.models import Category
from category.serializers import CategorySerializer


class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user  # Assuming user authentication is used
        # Filter categories where the menu owner is the authenticated user
        return Category.objects.filter(menu__owner=user)
