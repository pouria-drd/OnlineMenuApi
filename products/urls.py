from django.urls import path
from products.views import ProductListCreateAPIView, ProductDetailUpdateAPIView

urlpatterns = [
    path("", ProductListCreateAPIView.as_view(), name="product-list-create"),
    path(
        "<uuid:product_id>/",
        ProductDetailUpdateAPIView.as_view(),
        name="product-detail-update",
    ),
]
