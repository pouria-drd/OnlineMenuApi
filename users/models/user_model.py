import uuid
from django.db import models
from users.managers import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.validators import username_validator, iran_phone_validator, email_validator


class UserModel(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that replaces Django's default user model.
    Uses UUID as the primary key, enforces unique usernames, and supports both email and phone authentication.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Email is required for user creation
    email = models.EmailField(
        unique=True,
        blank=False,  # Email is required
        null=False,
        validators=[email_validator],  # Apply email validator
        help_text="Enter a valid email address.",
    )

    # Username is required and must be unique
    username = models.CharField(
        unique=True,
        max_length=25,
        validators=[username_validator],  # Apply username validator
        help_text="Required. 25 characters or fewer. Letters, digits, and _ only.",
    )

    # Phone number is optional
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        blank=True,  # Phone number is optional
        null=True,
        validators=[iran_phone_validator],  # Apply phone number validator
        help_text="Enter a valid Iranian phone number (e.g., +989123456789 or 09123456789).",
    )

    # Optional last name field, can be left blank or set to null.
    last_name = models.CharField(max_length=30, blank=True, null=True)

    # Optional first name field, can be left blank or set to null.
    first_name = models.CharField(max_length=30, blank=True, null=True)

    # Boolean flags for account status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Attach the custom manager
    objects = UserManager()

    # Set the USERNAME_FIELD to 'username' for login
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]  # Only email is required for user creation

    # Timestamps for user creation and last update
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Meta class for the UserModel.
        """

        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ("-created_at",)

    def __str__(self):
        """
        String representation of the user.
        """
        return self.username

    def get_full_name(self):
        """
        Returns the full name of the user.
        """
        return f"{self.first_name} {self.last_name}".strip()

    def save(self, *args, **kwargs):
        """
        Override save method to ensure the username is always stored in lowercase.
        """
        self.username = self.username.lower()  # Ensure username is in lowercase

        super().save(*args, **kwargs)
