from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("cst/", include("customer_panel.urls")),
    path("categories/", include("categories.urls")),
]

if settings.DEBUG:
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
