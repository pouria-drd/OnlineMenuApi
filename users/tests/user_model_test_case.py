import uuid
from django.test import TestCase
from users.models import UserModel


class UserModelTestCase(TestCase):
    """Test cases for the custom UserModel"""

    def setUp(self):
        """Create a test user before running each test"""
        self.user = UserModel.objects.create_user(
            email="user@example.com",
            username="testuser",
            phone_number="+989123456789",
            password="UserPass123!",
        )

    def test_str_representation(self):
        """Ensure the __str__ method returns the username"""
        self.assertEqual(str(self.user), "testuser")

    def test_get_full_name(self):
        """Test full name retrieval when both first and last name are set"""
        self.user.first_name = "John"
        self.user.last_name = "Doe"
        self.user.save()
        self.assertEqual(self.user.get_full_name(), "John Doe")

    def test_get_full_name_with_only_first_name(self):
        """Ensure get_full_name works when only first name is set"""
        self.user.first_name = "John"
        self.user.last_name = ""
        self.user.save()
        self.assertEqual(self.user.get_full_name(), "John")

    def test_get_full_name_with_only_last_name(self):
        """Ensure get_full_name works when only last name is set"""
        self.user.first_name = ""
        self.user.last_name = "Doe"
        self.user.save()
        self.assertEqual(self.user.get_full_name(), "Doe")

    def test_get_full_name_with_no_names(self):
        """Ensure get_full_name returns an empty string if no names are set"""
        self.user.first_name = ""
        self.user.last_name = ""
        self.user.save()
        self.assertEqual(self.user.get_full_name(), "")

    def test_user_created_with_uuid(self):
        """Ensure that a user is assigned a UUID primary key"""
        self.assertIsNotNone(self.user.id)  # Ensure an ID exists
        self.assertIsInstance(self.user.id, uuid.UUID)  # Ensure it's a UUID field

    def test_updated_at_changes_on_save(self):
        """Ensure that 'updated_at' field changes when user is saved"""
        old_updated_at = self.user.updated_at  # Get current timestamp
        self.user.first_name = "UpdatedName"
        self.user.save()  # Save user with new data
        self.assertNotEqual(
            self.user.updated_at, old_updated_at
        )  # Ensure timestamp updated
