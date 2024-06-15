from django.urls import path
from categories.views import CategoryListCreateAPIView, CategoryDetailUpdateAPIView

urlpatterns = [
    path("", CategoryListCreateAPIView.as_view(), name="category-list-create"),
    path(
        "<uuid:category_id>/",
        CategoryDetailUpdateAPIView.as_view(),
        name="category-detail-update",
    ),
]
