from django.urls import path
from owner_panel.views import (
    CategoryListCreateAPIView,
    CategoryDetailUpdateAPIView,
    ProductDetailUpdateAPIView,
    ProductListCreateAPIView,
)

urlpatterns = [
    path(
        "<slug:menu_slug>/categories/",
        CategoryListCreateAPIView.as_view(),
        name="category-list-create",
    ),
    path(
        "<slug:menu_slug>/categories/<uuid:category_id>/",
        CategoryDetailUpdateAPIView.as_view(),
        name="category-detail-update",
    ),
    path(
        "<slug:menu_slug>/categories/<uuid:category_id>/products/",
        ProductListCreateAPIView.as_view(),
        name="product-list-create",
    ),
    path(
        "<slug:menu_slug>/categories/<uuid:category_id>/products/<uuid:product_id>/",
        ProductDetailUpdateAPIView.as_view(),
        name="product-detail-update",
    ),
]
