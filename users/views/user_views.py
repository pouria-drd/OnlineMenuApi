from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from users.serializers import UserSerializer


class UserDetailView(APIView):
    """
    API endpoint to retrieve the details of the authenticated user.
    """

    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def get(self, request: Request, *args, **kwargs):
        """
        Handle GET request for user details.
        Only returns the details of the authenticated user.
        """

        # Get the currently authenticated user from the request
        user = request.user

        # Serialize the user data using the UserSerializer
        serializer = UserSerializer(user)

        # Return a successful response with the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
