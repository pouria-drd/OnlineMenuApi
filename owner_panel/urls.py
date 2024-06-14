from django.urls import path
from owner_panel.views import (
    CategoryListCreateAPIView,
    CategoryDetailUpdateAPIView,
)

urlpatterns = [
    path(
        "<slug:menu_slug>/categories/",
        CategoryListCreateAPIView.as_view(),
        name="category-list-create",
    ),
    path(
        "<slug:menu_slug>/categories/<uuid:pk>/",
        CategoryDetailUpdateAPIView.as_view(),
        name="category-detail-update",
    ),
]
