from django.contrib import admin
from django.conf import settings
from django.urls import path, include

from rest_framework import routers

from menus.views import MenuViewSet
from categories.views import CategoryViewSet


router = routers.DefaultRouter()
router.register(r"menus", MenuViewSet)
router.register(r"categories", CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]

if settings.DEBUG:
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)
