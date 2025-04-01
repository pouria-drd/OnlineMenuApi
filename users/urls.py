from django.urls import path
from users.views import UserDetailView

urlpatterns = [
    path("me/", UserDetailView.as_view(), name="user-detail"),
]
