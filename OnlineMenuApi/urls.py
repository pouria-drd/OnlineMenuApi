from django.contrib import admin
from django.conf import settings
from django.urls import path, include

from rest_framework import routers

from menus.views import MenuViewSet
from categories.views import CategoryViewSet
from products.views import ProductViewSet, ProductPriceViewSet


router = routers.DefaultRouter()
router.register(r"menus", MenuViewSet)
router.register(r"categories", CategoryViewSet)

router.register(r"products", ProductViewSet)
router.register(r"product-price", ProductPriceViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]

if settings.DEBUG:
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)
