from users.serializers import UserSerializer
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle


class UserInfoView(RetrieveAPIView):
    """
    API endpoint to retrieve the details of the authenticated user.
    """

    http_method_names = ["get"]
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def get_object(self):
        return self.request.user
