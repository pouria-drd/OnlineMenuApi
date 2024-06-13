from django.urls import path

from customer.views import CustomerCategoryListAPIView

urlpatterns = [
    path(
        "<slug:menu_slug>/",
        CustomerCategoryListAPIView.as_view(),
        name="customer-category-list",
    ),
    # path(
    #     "<slug:menu_slug>/<slug:category_slug>/",
    #     CategoryListAPIView.as_view(),
    #     name="customer-product-list",
    # ),
]
