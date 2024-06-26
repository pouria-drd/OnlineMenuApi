from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class MyTokenObtainPairView(TokenObtainPairView):

    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class MyTokenRefreshView(TokenRefreshView):

    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)
