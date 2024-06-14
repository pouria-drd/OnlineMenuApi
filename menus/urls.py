from django.urls import path

from menus.views import CustomerMenuCategoryListView

urlpatterns = [
    path(
        "<slug:menu_slug>/",
        CustomerMenuCategoryListView.as_view(),
        name="customer-menu-category-list",
    ),
]
