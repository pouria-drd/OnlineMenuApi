import uuid
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

from users.managers import UserManager

USER_TYPE_CHOICES = (
    ("admin", _("Admin")),
    ("owner", _("Owner")),
)

# Custom username validator
username_validator = RegexValidator(
    regex=r"^[a-z0-9_]{1,25}$",
    message=_(
        "Username can only contain lowercase letters, numbers, and underscores and must be at most 25 characters long."
    ),
    code="invalid_username",
)

# Iranian phone number validator
iran_phone_number_validator = RegexValidator(
    regex=r"^(\+98|0)?9\d{9}$",
    message=_("Phone number must be in the format '+989xxxxxxxxx' or '09xxxxxxxxx'."),
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

    # Apply the username validator to the username field
    username = models.CharField(
        _("username"),
        unique=True,
        max_length=25,
        help_text=_("Required. 25 characters or fewer. Letters, digits and _ only."),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    email = models.EmailField(
        _("email address"),
        null=True,
        blank=True,
        unique=True,
        validators=[validate_email],
        error_messages={
            "unique": _("A user with that email address already exists."),
        },
    )

    # Add phone number field
    phone_number = models.CharField(
        _("Phone Number"),
        null=True,
        blank=True,
        unique=True,
        max_length=13,
        validators=[iran_phone_number_validator],
    )

    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def save(self, *args, **kwargs):
        # If email is an empty string, set it to None
        if self.email == "":
            self.email = None
        super(User, self).save(*args, **kwargs)
