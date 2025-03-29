from django.core.validators import RegexValidator, EmailValidator

# ----------------------------------
# Username Validator
# ----------------------------------

username_validator = RegexValidator(
    regex=r"^[a-z0-9_]{1,25}$",
    message="Username can only contain lowercase letters, numbers, and underscores and must be at most 25 characters long.",
    code="invalid_username",
)

# ----------------------------------
# Iranian Phone Number Validator
# ----------------------------------

iran_phone_validator = RegexValidator(
    regex=r"^(?:\+98|0)?9\d{9}$",
    message="Enter a valid Iranian phone number (e.g., +989123456789 or 09123456789).",
    code="invalid_phone",
)

# ----------------------------------
# Email Validator
# ----------------------------------

email_validator = EmailValidator(
    message="Enter a valid email address.",
    code="invalid_email",
)
