from logging import getLogger
from django.db.models import Q
from users.models import UserModel
from django.utils.timezone import now
from django.contrib.auth.backends import BaseBackend

logger = getLogger("login_v1")


class AuthBackend(BaseBackend):
    """
    Custom authentication backend that allows authentication using email, username, or phone number.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate a user by checking if the given `username` (which can be email, username, or phone)
        matches a user and the password is correct.
        """
        user = UserModel.objects.filter(
            Q(email=username) | Q(username=username) | Q(phone_number=username)
        ).first()

        if user and user.check_password(password):
            # Log successful login with timestamp
            message = (
                f"Successful login! URL: {request.build_absolute_uri()}, "
                f"Username: {username}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, Time: {now()}\n"
            )

            logger.info(message)

            return user

        # Log failed attempt with timestamp
        message = (
            f"Failed login attempt! URL: {request.build_absolute_uri()}, "
            f"Username: {username}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, Time: {now()}\n"
        )

        logger.warning(message)

        return None

    def get_user(self, user_id):
        """
        Retrieve a user instance based on the user ID.
        """
        return UserModel.objects.filter(pk=user_id).first()
