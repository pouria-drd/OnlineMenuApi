from django.urls import path
from owner_panel.views import CategoryCreateAPIView

urlpatterns = [
    path(
        "<slug:menu_slug>/",
        CategoryCreateAPIView.as_view(),
        name="list-create-category",
    ),
]
