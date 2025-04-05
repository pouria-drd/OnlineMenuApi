from django.urls import path
from users.views import UserInfoView, LoginView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("user-info/", UserInfoView.as_view(), name="user-info"),
    # path("logout/", LogoutView.as_view(), name="logout"),
    # path("refresh/", CookieTokenRefreshView.as_view(), name="token-refresh"),
]
