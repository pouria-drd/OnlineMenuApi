from django.test import TestCase
from django.core.exceptions import ValidationError
from users.validators import username_validator, iran_phone_validator, email_validator


class ValidatorTestCase(TestCase):
    """Test case for custom regex validators"""

    def test_valid_usernames(self):
        """Test that valid usernames pass the validator"""
        valid_usernames = ["user_1", "testuser", "hello123", "abc_123"]
        for username in valid_usernames:
            try:
                username_validator(username)  # Should not raise an error
            except ValidationError:
                self.fail(f"Valid username '{username}' raised a ValidationError!")

    def test_invalid_usernames(self):
        """Test that invalid usernames raise a ValidationError"""
        invalid_usernames = [
            "UserName",
            "test user",
            "user@name",
            "verylongusername_exceeding_25_chars",
        ]
        for username in invalid_usernames:
            with self.assertRaises(ValidationError):
                username_validator(username)

    def test_valid_iranian_phone_numbers(self):
        """Test that valid Iranian phone numbers pass the validator"""
        valid_phones = ["09123456789", "+989123456789", "09912345678"]
        for phone in valid_phones:
            try:
                iran_phone_validator(phone)  # Should not raise an error
            except ValidationError:
                self.fail(f"Valid phone number '{phone}' raised a ValidationError!")

    def test_invalid_iranian_phone_numbers(self):
        """Test that invalid Iranian phone numbers raise a ValidationError"""
        invalid_phones = ["123456789", "09123", "+989123456", "098765432112345"]
        for phone in invalid_phones:
            with self.assertRaises(ValidationError):
                iran_phone_validator(phone)

    def test_valid_emails(self):
        """Test that valid emails pass the validator"""
        valid_emails = ["user@example.com", "test.user@domain.net", "email123@xyz.org"]
        for email in valid_emails:
            try:
                email_validator(email)  # Should not raise an error
            except ValidationError:
                self.fail(f"Valid email '{email}' raised a ValidationError!")

    def test_invalid_emails(self):
        """Test that invalid emails raise a ValidationError"""
        invalid_emails = ["userexample.com", "user@.com", "user@domain", "@example.com"]
        for email in invalid_emails:
            with self.assertRaises(ValidationError):
                email_validator(email)
