import uuid
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

# Define user type choices
USER_TYPE_CHOICES = (
    ("admin", _("Admin")),
    ("owner", _("Owner")),
    ("customer", _("Customer")),
)

# Custom username validator
username_validator = RegexValidator(
    regex=r"^[a-z0-9_]{1,25}$",
    message=_(
        "Username can only contain lowercase letters, numbers, and underscores and must be at most 25 characters long."
    ),
    code="invalid_username",
)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Add user type field
    user_type = models.CharField(
        _("User Type"),
        choices=USER_TYPE_CHOICES,
        max_length=20,
        default="owner",
    )

    # Add username validator
    username_validator = username_validator

    # Apply the username validator to the username field
    username = models.CharField(
        _("username"),
        max_length=25,
        unique=True,
        help_text=_("Required. 25 characters or fewer. Letters, digits and _ only."),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    email = models.EmailField(
        _("email address"), unique=True, validators=[validate_email]
    )

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()
