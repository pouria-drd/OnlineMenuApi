from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from users.serializers import LoginUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.throttling import ScopedRateThrottle


class LoginView(APIView):
    """API endpoint to login a user."""

    http_method_names = ["post"]
    permission_classes = [AllowAny]

    throttle_scope = "anon"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request):
        serializer = LoginUserSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():

            user = serializer.validated_data["user"]

            refresh = RefreshToken.for_user(user)

            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response(
                data={
                    "cct": access_token,
                    "rft": refresh_token,
                    "message": "ورود موفیت آمیز بود!",
                },
                status=status.HTTP_200_OK,
            )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
