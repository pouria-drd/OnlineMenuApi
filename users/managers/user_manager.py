from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom manager for the UserModel, handling user and superuser creation.
    """

    def create_user(self, email=None, username=None, phone_number=None, password=None):
        """
        Creates and returns a regular user.
        """
        # Ensure that the user has an email
        if not email:
            raise ValueError("Users must have an email")

        # Ensure that the user has a username
        if not username:
            raise ValueError("Users must have a username")

        # Ensure that the user has a password
        if not password:
            raise ValueError("Users must have a password")

        email = self.normalize_email(email) if email else None  # Normalize email
        username = username.lower()  # Convert username to lowercase for uniqueness

        # Create the user instance with the provided details
        user = self.model(email=email, username=username, phone_number=phone_number)
        user.set_password(password)  # Hash the password before saving
        user.save(using=self._db)  # Save the user to the database

        return user

    def create_superuser(self, email, username, phone_number=None, password=None):
        """
        Creates and returns a superuser with all permissions.
        """
        # Set the phone number to None by default if not provided
        if not phone_number:
            phone_number = None

        user = self.create_user(
            email=email, username=username, phone_number=phone_number, password=password
        )
        user.is_superuser = True  # Assign superuser status
        user.is_staff = True  # Allow admin panel access

        user.save(using=self._db)

        return user
