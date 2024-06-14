from django.urls import path

from customer_panel.views import CustomerCategoryListView, CustomerCategoryDetailView


urlpatterns = [
    path(
        "<slug:menu_slug>/",
        CustomerCategoryListView.as_view(),
        name="customer-category-list",
    ),
    path(
        "<slug:menu_slug>/<uuid:category_id>/",
        CustomerCategoryDetailView.as_view(),
        name="customer-category-detail",
    ),
]
